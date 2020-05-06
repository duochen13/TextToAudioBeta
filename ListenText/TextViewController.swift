//
//  TextViewController.swift
//  ListenText
//
//  Created by Duo Chen on 5/1/20.
//  Copyright © 2020 Duo Chen. All rights reserved.
//

import UIKit
import MessageUI

class TextViewController: UIViewController, MFMailComposeViewControllerDelegate {
    

    // text sent from last VC
    var target_label_text: String?
    // bool var devides whether display summary_label
    var click_summary_button: Bool = false
    
    @IBOutlet weak var summary_label: UILabel!
    @IBOutlet weak var target_label: UILabel!
    @IBOutlet weak var static_summary_label: UILabel!
    @IBOutlet weak var export_button: UIBarButtonItem!
    
    struct SummaryText: Decodable {
        let summary_text: String
    }
    
    @IBAction func generate_summary(_ sender: Any) {
        // update bbol var to decides whether display summary label
        if (click_summary_button) {
            summary_label.text = ""
            click_summary_button = false
            return
        }
        click_summary_button = true
        
        // local url: http://localhost:5000/test
        // public url: http://298bdeb7.ngrok.io/test
        let url = URL(string: "http://localhost:5000/summary")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Serialize the json data
        let json = ["raw_text": target_label_text ?? ""]
        let jsonData = try! JSONSerialization.data(withJSONObject: json)
        request.httpBody = jsonData
                
        // running an async task in submitClicked
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            guard let _ = data, error == nil else {
                print("NETWORK ERROR")
                return
            }
            // parsing response
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                    print("HTTP STATUS: \(httpStatus.statusCode)")
                    return
                    }
                    // parse json
                    if let data = data {
                        do {
                            let res = try JSONDecoder().decode(SummaryText.self, from:data)
                            
                            print("raw.summary_text", res.summary_text)
                            
                            DispatchQueue.main.async {
                                self.summary_label.text = res.summary_text
                            }
                            
                        } catch let error {
                            print(error)
                        }
                    }
        }
        task.resume()
        
    }
    
    @IBAction func export_action(_ sender: Any) {
        sendEmail()
    }
    
    func sendEmail() {
        if MFMailComposeViewController.canSendMail() {
            let mail = MFMailComposeViewController()
            mail.mailComposeDelegate = self
            mail.setToRecipients(["duochen@umich.edu"])
            mail.setSubject("Test Subject")
            mail.setMessageBody("Hello", isHTML: false)
            present(mail, animated: true, completion: nil)
        } else {
            print("fault encountered!")
        }
    }
    
    func mailComposeController(_ controller: MFMailComposeViewController, didFinishWith result: MFMailComposeResult, error: Error?) {
         dismiss(animated: true, completion: nil)
    }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // set up global variables
        target_label.text = "  \(target_label_text ?? "No text found")!"
        summary_label.text = ""
        // setup UI components
        target_label.numberOfLines = 0
        target_label.sizeToFit()
        target_label.font = UIFont(name: "Helvetica", size: 20.0)
        // font ref: https://github.com/lionhylra/iOS-UIFont-Names
        summary_label.font = UIFont(name: "MarkerFelt-Wide", size: 20.0)
        static_summary_label.font = UIFont(name: "BodoniOrnamentsITCTT", size: 28.0)
    }
    

}
