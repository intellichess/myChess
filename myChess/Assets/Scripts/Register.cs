using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Text.RegularExpressions;
using UnityEngine.UI;

public class Register : MonoBehaviour {
	public GameObject name;
	public GameObject password;
	private string Name;
	private string Password;
	private string form;
	// Use this for initialization
	void Start () {
		
	}

	public void Submit(){
		bool UN = false;
		bool PW = false;
		if (Name != "") {
			if (!System.IO.File.Exists (@"E:/UnityTestFolder/" + Name + ".txt")) {
				UN = true;
			} else {
				print ("TEST");
				Debug.LogWarning ("Username Taken");
			}
		} else {
			Debug.LogWarning ("Username Field Empty");
		}
		if (Password != "") {
			if (Password.Length > 5) {
				PW = true;
			} else {
				Debug.LogWarning ("Password must be at least 6 characters.");
			}
		} else {
			Debug.LogWarning ("Password Field Empty");
		}
		if (UN == true && PW == true) {
			form = (Name + "\n" + Password);
			System.IO.File.WriteAllText (@"E:/UnityTestFolder/" + Name + ".txt",form);
			Name = name.GetComponent<InputField> ().text = "";
			Password = password.GetComponent<InputField> ().text = "";
			print ("Registration Complete");
		}
			
	}


	// Update is called once per frame
	void Update () {
		//add a tab and return function to input fields to allow a little more user friendly expierience.
		if (Input.GetKeyDown (KeyCode.Tab) || Input.GetKeyDown (KeyCode.Return)) {
			if (name.GetComponent<InputField> ().isFocused) {
				password.GetComponent<InputField> ().Select ();
			}
		}
		if (Input.GetKeyDown (KeyCode.Return)) {
			if (Name != "" && Password != "") {
				Submit ();
			}
		}

		Name = name.GetComponent<InputField> ().text;
		Password = password.GetComponent<InputField> ().text;
	}
}
