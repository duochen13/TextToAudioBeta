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
    
    
    @IBAction func testPostRequest(_ sender: Any) {
    }
    
    
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
        
        let url = URL(string: "http://localhost:5000/test")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue(Bundle.main.bundleIdentifier ?? "", forHTTPHeaderField: "X-Ios-Bundle-Identifier")
        
        let json = ["content": imageBase64]
        
        // Serialize the JSON
        let jsonData = try! JSONSerialization.data(withJSONObject: json)
        request.httpBody = jsonData
        
        print("jsonData: ", jsonData)
        
        // running an async task in submitClicked
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            guard let _ = data, error == nil else {
                print("NETWORK ERROR")
                return
            }
            print("response data: ", data)
            
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                print("HTTP STATUS: \(httpStatus.statusCode)")
                return
            }
        }
        task.resume()
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }


}

