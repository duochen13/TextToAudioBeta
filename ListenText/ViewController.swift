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
    
    @IBOutlet weak var target_label: UILabel!
    @IBOutlet weak var take_photo_button: UIButton!
    
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
            // send image to server

        }
        
        self.target_label.text = ""
        
        imagePicker.dismiss(animated: true, completion: nil)
    }
    
    func resizeImage(_ imageSize: CGSize, image: UIImage) -> Data {
        UIGraphicsBeginImageContext(imageSize)
        image.draw(in: CGRect(x: 0, y: 0, width: imageSize.width, height: imageSize.height))
        let newImage = UIGraphicsGetImageFromCurrentImageContext()
        let resizedImage = newImage!.pngData()
        UIGraphicsEndImageContext()
        return resizedImage!
    }
    
    // usage: imagePickerController()
    func base64EncodeImage(_ image: UIImage) -> String {
        
        var imagedata = image.pngData()

        // Resize the image if it exceeds the 2MB API limit, to be added
        if (imagedata!.count > 2097152) {
            let oldSize: CGSize = image.size
            let newSize: CGSize = CGSize(width: 800, height: oldSize.height / oldSize.width * 800)
            imagedata = resizeImage(newSize, image: image)
        }
        
        return imagedata!.base64EncodedString(options: .endLineWithCarriageReturn)
    }
    
    struct Labels: Decodable {
        let labels: [String]
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
            // parsing response
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                    print("HTTP STATUS: \(httpStatus.statusCode)")
                    return
                    }
                    // parse json
                    if let data = data {
                        do {
                            let res = try JSONDecoder().decode(Labels.self, from:data)
            
                            print("raw.label", res.labels)
                            // self.raw_contents = res.sentence
                            // self.translated_contents = res.translates
                            
                            DispatchQueue.main.async {

//                                var appDelegate = UIApplication.shared.delegate as! AppDelegate
//                                context = appDelegate.persistentContainer.viewContext
                                self.target_label.text = res.labels[0]
                                
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
        // Do any additional setup after loading the view.
        self.take_photo_button.isEnabled = true

        self.target_label.text = ""
    }


}




extension UIImage {
    // MARK: - UIImage+Resize
    func compressTo(_ expectedSizeInMb:Int) -> UIImage? {
        let sizeInBytes = expectedSizeInMb * 1024 * 1024
        var needCompress:Bool = true
        var imgData:Data?
        var compressingValue:CGFloat = 1.0
        while (needCompress && compressingValue > 0.0) {
            if let data:Data = self.jpegData(compressionQuality: compressingValue) {
            if data.count < sizeInBytes {
                needCompress = false
                imgData = data
            } else {
                compressingValue -= 0.1
            }
        }
    }

    if let data = imgData {
        if (data.count < sizeInBytes) {
            return UIImage(data: data)
        }
    }
        return nil
    }
}
