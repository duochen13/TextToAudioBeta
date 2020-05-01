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
    
    @IBOutlet weak var target_label: UILabel!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        target_label.text = "  \(target_label_text ?? "No text found")!"
        // Do any additional setup after loading the view.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
