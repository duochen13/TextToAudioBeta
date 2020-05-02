//
//  TextViewController.swift
//  ListenText
//
//  Created by Duo Chen on 5/1/20.
//  Copyright © 2020 Duo Chen. All rights reserved.
//

import UIKit

class TextViewController: UIViewController {

    // text sent from last VC
    var target_label_text: String?
    
    @IBOutlet weak var summary_label: UILabel!
    @IBOutlet weak var target_label: UILabel!
    
    struct SummaryText: Decodable {
        let summary_text: String
    }
    
    @IBAction func generate_summary(_ sender: Any) {

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
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        target_label.text = "  \(target_label_text ?? "No text found")!"
        summary_label.text = ""
        // Do any additional setup after loading the view.
    }
    

}
