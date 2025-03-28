//
//  ContentView.swift
//  Haptic-Link
//
//  Created by Evan Woods on 3/27/25.
//

import SwiftUI

struct ContentView: View {
    @StateObject private var webSocketManager = WebSocketManager()

    var body: some View {
        VStack {
            Text("Mouse Click Listener")
                .font(.title)
                .padding()

            Text(webSocketManager.latestClick)
                .font(.headline)
                .foregroundColor(.blue)
                .padding()

            HStack {
                Button("Connect") {
                    webSocketManager.connect()
                }
                .padding()
                .background(Color.green)
                .foregroundColor(.white)
                .clipShape(Capsule())

                Button("Disconnect") {
                    webSocketManager.disconnect()
                }
                .padding()
                .background(Color.red)
                .foregroundColor(.white)
                .clipShape(Capsule())
            }
        }
    }
}


#Preview {
    ContentView()
}
