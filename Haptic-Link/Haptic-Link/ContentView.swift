import SwiftUI

struct ContentView: View {
    
    @StateObject private var bluetoothManager = BluetoothManager()
    
    var body: some View {
        NavigationView {
            List {
                ForEach(bluetoothManager.peripherals, id: \.identifier) { peripheral in
                    HStack {
                        Text(peripheral.name ?? "Unknown")
                        Spacer()
                        Button("Connect") {
                            bluetoothManager.connectToPeripheral(peripheral)
                        }
                    }
                }
            }
            .navigationBarTitle("Bluetooth Devices")
            .onAppear {
                bluetoothManager.startScanning()
            }
            .onDisappear {
                bluetoothManager.stopScanning()
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
