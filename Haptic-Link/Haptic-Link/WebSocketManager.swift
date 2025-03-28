import Foundation

class WebSocketManager: ObservableObject {
    private var webSocketTask: URLSessionWebSocketTask?
    @Published var latestClick: String = "No Clicks Yet"

    func connect() {
        guard let url = URL(string: "ws://192.168.1.250:8765") else {
            print("Invalid WebSocket URL")
            return
        }

        webSocketTask = URLSession.shared.webSocketTask(with: url)
        webSocketTask?.resume()
        receiveMessage()
    }

    func disconnect() {
        webSocketTask?.cancel(with: .goingAway, reason: nil)
    }

    private func receiveMessage() {
        webSocketTask?.receive { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success(let message):
                    switch message {
                    case .string(let text):
                        print("Received message: \(text)")
                        self?.latestClick = "Click at: \(text)"
                    default:
                        print("Received unknown data type")
                    }
                case .failure(let error):
                    print("WebSocket error: \(error)")
                }
                self?.receiveMessage() // Keep listening
            }
        }
    }
}
