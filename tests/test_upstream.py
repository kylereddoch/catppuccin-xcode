"""Compare native themes to an immutable, licensed upstream reference."""
import hashlib
import json
from pathlib import Path
import plistlib
import unittest

from test_themes import decode_hex, generate

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/upstream'


def flatten(data):
    return {f'{key}/{sub}' if sub else key: value
            for key, item in data.items()
            for sub, value in (item.items() if isinstance(item, dict) else [(None, item)])}


def legacy_hex(value):
    channels = [float(channel) for channel in value.split()]
    assert len(channels) == 4 and channels[3] == 1, value
    return '#' + ''.join(f'{round(channel * 255):02x}' for channel in channels[:3])


class UpstreamTests(unittest.TestCase):
    def test_reference_hashes_and_exhaustive_coverage(self):
        manifest = json.loads((FIXTURES / 'source.json').read_text())
        coverage = json.loads((ROOT / 'palettes/upstream-coverage.json').read_text())
        statuses = {'direct', 'separate-setting', 'metadata', 'approximation', 'unexposed', 'merged'}
        for flavor, entry in manifest['files'].items():
            with self.subTest(flavor=flavor):
                raw = (FIXTURES / f'{flavor}.xccolortheme').read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), entry['sha256'])
                self.assertEqual(set(flatten(plistlib.loads(raw))), set(coverage))
                for setting, disposition in coverage.items():
                    self.assertIn(disposition['status'], statuses, setting)
                    if disposition['status'] != 'direct':
                        self.assertTrue(disposition.get('note'), setting)

    def test_every_direct_native_color_matches_official_source(self):
        coverage = json.loads((ROOT / 'palettes/upstream-coverage.json').read_text())
        for flavor in generate.FLAVORS:
            source = flatten(plistlib.loads((FIXTURES / f'{flavor}.xccolortheme').read_bytes()))
            recipe = json.loads(generate.theme_path(flavor).read_text())['recipe']
            for setting, disposition in coverage.items():
                if disposition['status'] not in {'direct', 'approximation'}:
                    continue
                target = disposition['target']
                native = recipe['background']['customColor'] if target == 'background' else next(iter(recipe['palette']['colorOverrides'][target].values()))
                with self.subTest(flavor=flavor, setting=setting, target=target):
                    self.assertEqual(decode_hex(native), legacy_hex(source[setting]))

    def test_native_fallbacks_and_added_roles_are_intentional(self):
        mapping = json.loads((ROOT / 'palettes/mapping.json').read_text())
        for parent, child in {'projectType': 'projectType.type', 'otherType': 'otherType.type',
                              'projectMember': 'projectMember.function', 'otherMember': 'otherMember.function',
                              'commentEmphasized': 'comment'}.items():
            self.assertEqual(mapping[parent], mapping[child])
        self.assertEqual(mapping['diffAddition'], 'green')
        self.assertEqual(mapping['diffDeletion'], 'red')
        self.assertEqual(mapping['debugger'], 'green')


if __name__ == '__main__':
    unittest.main()
