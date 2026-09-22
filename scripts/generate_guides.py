#!/usr/bin/env python3
"""Generate repository color guides and SVG diagrams from the theme sources."""
import argparse
from html import escape
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
FLAVORS = ('latte', 'frappe', 'macchiato', 'mocha')
# Human-readable labels and examples for each native Xcode color assignment.
ROLES = {
    'plainText': ('Plain text', 'Punctuation and unclassified source text'),
    'comment': ('Comments', '// Take a coffee break'),
    'commentEmphasized': ('Emphasized comments', 'Comment emphasis / markers'),
    'markdown': ('Documentation comments', '/// A fresh cup of coffee'),
    'markdownEmphasized': ('Emphasized documentation', 'Emphasis inside documentation'),
    'keyword': ('Keywords', 'struct, let, var, func, return'),
    'keyword.attribute': ('Attributes', '@MainActor, @State'),
    'string': ('Strings', '"Coffee is ready"'),
    'string.regex': ('Regular expressions', '/[A-Z]+/'),
    'number': ('Numbers', '42, 3.14'),
    'number.character': ('Character literals', "'A' in a language with character literals"),
    'link': ('Links', 'URLs in source documentation'),
    'preprocessor': ('Preprocessor directives', '#if, #endif'),
    'preprocessor.macro': ('Project macros', 'A macro defined in your project'),
    'preprocessor.macroSystem': ('System macros', 'A macro supplied by the SDK'),
    'typeDeclaration': ('Type declarations', 'Coffee in struct Coffee'),
    'memberDeclaration': ('Member declarations', 'The declared property or function name'),
    'projectType': ('Project types — fallback', 'A type from your project'),
    'projectType.class': ('Project classes', 'A reference to your CoffeeStore class'),
    'projectType.type': ('Project type references', 'A reference to your Coffee type'),
    'projectMember': ('Project members — fallback', 'A member from your project'),
    'projectMember.function': ('Project functions', 'A call to your brew() function'),
    'projectMember.constant': ('Project constants', 'A reference classified as a project constant'),
    'projectMember.variable': ('Project variables', 'A reference classified as a project variable'),
    'otherType': ('External types — fallback', 'A type provided by a framework'),
    'otherType.class': ('External classes', 'A reference to an SDK class'),
    'otherType.type': ('External type references', 'String, Int, Text'),
    'otherMember': ('External members — fallback', 'A member provided by a framework'),
    'otherMember.function': ('External functions', 'print(), uppercased()'),
    'otherMember.constant': ('External constants', 'A reference classified as an SDK constant'),
    'otherMember.variable': ('External variables', 'A reference classified as an SDK variable'),
    'selectedTextBackgroundColor': ('Selection background', 'The fill behind selected text'),
    'insertionPointColor': ('Cursor color', 'Your text insertion point'),
    'currentLineHighlight': ('Current line background', 'The fill behind the active line'),
    'invisibles': ('Invisible characters', 'Visible whitespace markers when enabled'),
    'diffAddition': ('Diff additions', 'Added code in a comparison'),
    'diffDeletion': ('Diff deletions', 'Removed code in a comparison'),
    'debugger': ('Debugger', 'The debugger color supplied to Xcode'),
}


def diagram(flavor, palette, mapping):
    colors = palette['colors']
    def c(name): return colors[name]['hex']
    def role(name): return c(mapping[name])
    pieces = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="1190" viewBox="0 0 1100 1190" role="img" aria-labelledby="title description">
<title id="title">Catppuccin {escape(palette['name'])} color guide</title>
<desc id="description">Illustrative Swift syntax, labeled editor colors, and all 26 palette swatches. Exact mappings and hex values are also provided as text on the guide page. This is not an Xcode screenshot.</desc>
<rect width="1100" height="1190" rx="18" fill="{c('base')}"/>
<g font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">''']
    def rect(x, y, w, h, fill, stroke=None, radius=8):
        pieces.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')
    def text(x, y, value, fill=None, size=16, weight=400):
        pieces.append(f'<text x="{x}" y="{y}" fill="{fill or c("text")}" font-size="{size}" font-weight="{weight}">{escape(value)}</text>')
    text(32, 49, f"Catppuccin {palette['name']}", size=30, weight=650)
    text(32, 78, f"{'Dark' if palette['dark'] else 'Light'} appearance · Illustrative color guide · Background {c('base').upper()}", c('subtext1'))
    rect(32, 104, 648, 386, c('base'), c('surface2'))
    text(54, 135, 'SWIFT SYNTAX', c('subtext1'), 13, 650)
    # Each token uses the corresponding theme role, not a guessed RGB value.
    lines = [
        [('keyword','import '), ('otherType.type','SwiftUI')],
        [],
        [('markdown','/// A fresh cup of coffee.')],
        [('keyword.attribute','@MainActor')],
        [('keyword','struct '), ('typeDeclaration','Coffee'), ('plainText',' {')],
        [('plainText','    '), ('keyword','let '), ('memberDeclaration','id'), ('plainText',' = '), ('number','42')],
        [('plainText','    '), ('keyword','var '), ('memberDeclaration','name'), ('plainText',' = '), ('string',f'"{palette["name"]}"')],
        [],
        [('plainText','    '), ('keyword','func '), ('memberDeclaration','brew'), ('plainText','() -> '), ('otherType.type','String'), ('plainText',' {')],
        [('plainText','        '), ('comment','// Make something wonderful.')],
        [('plainText','        '), ('keyword','return '), ('projectMember.variable','name'), ('plainText','.'), ('otherMember.function','uppercased'), ('plainText','()')],
        [('plainText','    }')],
        [('plainText','}')],
    ]
    for i, tokens in enumerate(lines):
        spans = ''.join(f'<tspan fill="{role(key)}">{escape(value)}</tspan>' for key,value in tokens)
        pieces.append(f'<text x="54" y="{168 + i * 24}" xml:space="preserve" font-family="SFMono-Regular, Menlo, Consolas, monospace" font-size="17">{spans}</text>')
    legend=[('keyword','Keywords'),('keyword.attribute','Attributes / types'),('memberDeclaration','Functions / declarations'),('string','Strings'),('number','Numbers / constants'),('plainText','Plain text / variables'),('comment','Comments / documentation'),('string.regex','Regex / preprocessors'),('link','Links'),('markdownEmphasized','Documentation emphasis')]
    for i,(key,label) in enumerate(legend):
        y=116+i*37
        rect(706,y,18,18,role(key),radius=4)
        text(736,y+12,label,size=14,weight=550)
        text(736,y+28,f"{colors[mapping[key]]['name']} · {role(key).upper()}",c('subtext1'),12)
    text(32,532,'EDITOR COLORS',c('subtext1'),14,650)
    # Theme assignments are represented as swatches, not a mock Xcode interface.
    surfaces=[('currentLineHighlight','Current line'),('selectedTextBackgroundColor','Selection'),('insertionPointColor','Cursor'),('invisibles','Invisible characters'),('diffAddition','Diff additions'),('diffDeletion','Diff deletions'),('debugger','Debugger')]
    for i,(key,label) in enumerate(surfaces):
        col,row=i%4,i//4
        x,y=32+col*266,552+row*95
        rect(x,y,240,78,c('base'),c('surface2'))
        rect(x+12,y+14,28,48,role(key),radius=4)
        text(x+52,y+29,label,size=14,weight=600)
        text(x+52,y+49,colors[mapping[key]]['name'],c('subtext1'),12)
        text(x+52,y+65,role(key).upper(),c('subtext1'),12)
    text(32,781,'FULL PALETTE',c('subtext1'),14,650)
    for i,(name,color) in enumerate(sorted(colors.items(),key=lambda item:item[1]['order'])):
        x,y=32+(i%6)*177,806+(i//6)*64
        rect(x,y,28,42,color['hex'],c('surface2'),4)
        text(x+37,y+16,color['name'],size=13,weight=550)
        text(x+37,y+35,color['hex'].upper(),c('subtext1'),12)
    text(32,1160,'Generated from the repository palette and mappings. See the guide tables for exact assignments.',c('subtext1'),14)
    pieces.append('</g></svg>')
    return '\n'.join(pieces)+'\n'


def guide(flavor, palette, mapping):
    name=palette['name']
    colors=palette['colors']
    navigation=' · '.join(f'[{key.title() if key != "frappe" else "Frappé"}]({key}.md)' for key in FLAVORS)
    rows=[]
    for role,color in mapping.items():
        label,example=ROLES[role]
        rows.append(f"| {label} | {example} | {colors[color]['name']} | `{colors[color]['hex'].upper()}` |")
    theme=quote(f'Catppuccin {name}.xcworkspacecolortheme')
    used=set(mapping.values())|{'base','lavender'}
    palette_rows='\n'.join(f"| {entry['name']} | `{entry['hex'].upper()}` | {'Used by this theme' if key in used else 'Available in palette; not explicitly assigned'} |" for key,entry in sorted(colors.items(),key=lambda item:item[1]['order']))
    return f'''<!-- Generated by scripts/generate_guides.py; edit the sources, then regenerate. -->
# Catppuccin {name}

[All themes](../../README.md#themes-and-status) · {navigation}

**{'Dark' if palette['dark'] else 'Light'} appearance** · [Theme file](../../themes/{theme}) · [Installation instructions](../../README.md#install)

## Color example

![{name} syntax example, labeled editor colors, and palette swatches](../assets/{flavor}-guide.svg)

This is a generated color diagram, not an Xcode screenshot. It uses the exact palette and semantic assignments in this repository. Xcode chooses token categories based on language and context, so the same word can receive different colors in real code. The full mapping is available as readable text below.

## Background and interface

| Setting | Palette color | Hex | What it affects |
| --- | --- | --- | --- |
| Background | Base | `{colors['base']['hex'].upper()}` | Solid background supplied to the workspace theme |
| Foreground seed | Lavender | `{colors['lavender']['hex'].upper()}` | Starting color for Xcode-generated interface colors |
| Background seed | Base | `{colors['base']['hex'].upper()}` | Starting color for Xcode-generated background treatments |

Other workspace surfaces, console colors, and status treatments are derived by Xcode. They are not independently assigned exact colors by this theme. Fonts and cursor shape are separate settings.

## What each color controls

All **38 explicit assignments** are listed here. “Fallback” is the broader category used when a more specific category is unavailable; specific assignments appear in their own rows.

| Xcode element | Example or use | Palette color | Hex |
| --- | --- | --- | --- |
{chr(10).join(rows)}

## Palette reference

These are all 26 official {name} colors. A color being in the palette does not mean Xcode uses it as an explicit override.

| Color | Hex | Use in this theme |
| --- | --- | --- |
{palette_rows}

## Try it

```sh
sh install.sh {flavor}
```

Run this from the downloaded repository, restart Xcode when convenient, then select **Catppuccin {name}** in **Settings → Appearance → Theme → Choose…**. Use **{'Dark' if palette['dark'] else 'Light'}** appearance.

The diagrams describe the intended mappings; they do not establish that every Xcode surface has been visually tested. See the [verification record](../VERIFICATION.md) for the current testing status.
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Verify generated guides without writing files.')
    args=parser.parse_args()
    palettes=json.loads((ROOT/'palettes/catppuccin.json').read_text())
    mapping=json.loads((ROOT/'palettes/mapping.json').read_text())
    if set(mapping)!=set(ROLES):
        parser.error('Guide labels must cover every mapping key, with no extras.')
    stale=[]
    for flavor in FLAVORS:
        outputs={ROOT/f'docs/themes/{flavor}.md':guide(flavor,palettes[flavor],mapping),ROOT/f'docs/assets/{flavor}-guide.svg':diagram(flavor,palettes[flavor],mapping)}
        for path,content in outputs.items():
            if args.check:
                if not path.exists() or path.read_text()!=content: stale.append(str(path.relative_to(ROOT)))
            else:
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text(content)
                print(f'Generated {path.relative_to(ROOT)}')
    if stale: parser.exit(1,'Guides need regeneration: '+', '.join(stale)+'\n')
    if args.check: print('Generated color guides are current.')


if __name__=='__main__':
    main()
