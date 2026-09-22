import SwiftUI

// MARK: - Catppuccin Mocha

/// A quiet workspace with warm, pastel syntax colors.
struct MochaPreview: View {
    @State private var cups = 2
    private let title = "Make something wonderful."

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Label("Catppuccin Mocha", systemImage: "cup.and.saucer.fill")
                .font(.title.bold())

            Text(title)
                .foregroundStyle(.secondary)

            Stepper("Coffee: \(cups)", value: $cups, in: 0...10)

            Button("Take a break") {
                cups += 1
                print("A fresh cup, a fresh perspective.")
            }
        }
        .padding(24)
    }
}
