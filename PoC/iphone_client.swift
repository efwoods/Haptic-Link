import UIKit
import AudioToolbox

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        startListeningForSignal()
    }
    
    func startListeningForSignal() {
        let url = URL(string: "http://<your-pc-ip>:5000/vibrate")! // Replace with your PC's IP
        
        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            if let _ = data, error == nil {
                // Trigger vibration
                AudioServicesPlaySystemSound(kSystemSoundID_Vibrate)
            }
        }
        
        task.resume()
    }
}
