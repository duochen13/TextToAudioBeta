//
//  ViewController.swift
//  ListenText
//
//  Created by Duo Chen on 4/23/20.
//  Copyright © 2020 Duo Chen. All rights reserved.
//

import UIKit
import AVFoundation
import SwiftyJSON

class ViewController: UIViewController, UINavigationControllerDelegate, UIImagePickerControllerDelegate {
    
    var imagePicker: UIImagePickerController!
    var googleAPIKey = ""
    var googleURL: URL {
        return URL(string: "https://vision.googleapis.com/v1/images:annotate?key=\(googleAPIKey)")!
    }
    let session = URLSession.shared
    
    @IBOutlet weak var imageView: UIImageView!
    
    @IBAction func takePhoto(_ sender: Any) {
        imagePicker = UIImagePickerController()
        imagePicker.delegate = self
        
        //imagePicker.sourceType = .camera
        imagePicker.sourceType = .photoLibrary
        
        present(imagePicker, animated:  true, completion: nil)
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        
        if let pickedImage = info[UIImagePickerController.InfoKey.originalImage] as? UIImage {
            imageView.image = info[.originalImage] as? UIImage
            
            // Encode the image (result is String)
            let binaryImageData = base64EncodeImage(pickedImage)
            createRequest(with: binaryImageData)
        }
        
        imagePicker.dismiss(animated: true, completion: nil)
    
        // send image to server
        
    }
    
    // usage: imagePickerController()
    func base64EncodeImage(_ image: UIImage) -> String {
        let imagedata = image.pngData()
        // Resize the image if it exceeds the 2MB API limit, to be added
        return imagedata!.base64EncodedString(options: .endLineWithCarriageReturn)
    }
    
    // usage: imagePickerController()
    func createRequest(with imageBase64: String) {
        var request = URLRequest(url: googleURL)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue(Bundle.main.bundleIdentifier ?? "", forHTTPHeaderField: "X-Ios-Bundle-Identifier")
        // Build our API request
        let jsonRequest = [
            "requests": [
                "image": [
                    "content": imageBase64
                ],
                "features": [
                    [
                        "type": "LABEL_DETECTION",
                        "maxResults": 10
                    ]
                ]
            ]
        ]
        // Serialize the JSON
        let jsonData = try! JSONSerialization.data(withJSONObject: jsonRequest, options: [])
        
        request.httpBody = jsonData
        print("jsonData: ", jsonData)
        
        let task: URLSessionDataTask = session.dataTask(with: request) { (data, response, error) in
            guard let data = data, error == nil else {
                print(error?.localizedDescription ?? "")
                return
            }
            print("data: ", data)
            // self.analyzeResults(data)
        }
        
        task.resume()
        
        
        task.resume()
        
        // Serialize the JSON
//        guard let data = try? jsonObject.rawData() else {
//            return
//        }
//        request.httpBody = data
        // Run the request on a background thread
        
        
        // DispatchQueue.global().async { self.runRequestOnBackgroundThread(request) }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }


}

