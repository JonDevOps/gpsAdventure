//Get Data
function formatData(div, url, prefix, suffix)
{
	var XMLHTTP= XMLHttpRequest || ActiveXObject("Microsoft.XMLHTTP");
	if (typeof XMLHTTP!= "undefined" ) 
	{
		var xmlhttp = new XMLHTTP;
		xmlhttp.onreadystatechange= function() {
			if(xmlhttp.readyState== 4) //4 is recv'd all responses
			{
				var resp = xmlhttp.responseText;
				document.getElementById(div).innerHTML= prefix + resp + suffix;				
			}			
		}
		xmlhttp.open("GET", url , true);
		xmlhttp.send(null);
	}
	else
		alert("Your browser doesn't seem to support ajax");
}

//Get Data
function loadData(div, url)
{
	var XMLHTTP= XMLHttpRequest || ActiveXObject("Microsoft.XMLHTTP");
	if (typeof XMLHTTP!= "undefined" ) 
	{
		var xmlhttp = new XMLHTTP;
		xmlhttp.onreadystatechange= function() {
			if(xmlhttp.readyState== 4) //4 is recv'd all responses
			{
				var resp = xmlhttp.responseText;
				if (div=="log")
				{
					document.getElementById(div).innerHTML+= resp;
				}
				else
				{
					document.getElementById(div).innerHTML= resp;
				}
			}			
		};
		xmlhttp.open("GET", url , true);
		xmlhttp.send(null);
	}
	else
		alert("Your browser doesn't seem to support ajax");
}

function postDataLogin(url)
{
var serialized = $('form').serialize();
//alert(serialized);
var XMLHTTP= XMLHttpRequest || ActiveXObject("Microsoft.XMLHTTP");
	if (typeof XMLHTTP!= "undefined" ) 
	{
		var xmlhttp = new XMLHTTP;
		xmlhttp.onreadystatechange = function() {
			var resp = xmlhttp.responseText;
			document.getElementById('temp').innerHTML = resp;
			if (resp.indexOf("You") >= 0)
			{				
				location.reload(true);
			}
		};
		xmlhttp.open("POST", url , true);
		xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		xmlhttp.send(serialized);
		
	}
	else
		alert("Your browser doesn't seem to support ajax");

}

function postData(url)
{
var serialized = $('form').serialize();
//alert(serialized + "\nurl:" + url );
var XMLHTTP= XMLHttpRequest || ActiveXObject("Microsoft.XMLHTTP");
	if (typeof XMLHTTP!= "undefined" ) 
	{
		var xmlhttp = new XMLHTTP;
		xmlhttp.onreadystatechange = function() {
			var resp = xmlhttp.responseText;
			document.getElementById('temp').innerHTML = resp;
		}
		xmlhttp.open("POST", url , true);
		xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
		xmlhttp.send(serialized);
	}
	else
		alert("Your browser doesn't seem to support ajax");

}

function postDataDivClear(div, url, clearIf, doAfter)
{
var serialized = $('form').serialize();
//alert(serialized + "\nurl:" + url );
var XMLHTTP= XMLHttpRequest || ActiveXObject("Microsoft.XMLHTTP");
	if (typeof XMLHTTP!= "undefined" ) 
	{
		var xmlhttp = new XMLHTTP;
		xmlhttp.onreadystatechange = function() {
			var resp = xmlhttp.responseText;
			document.getElementById(div).innerHTML = resp;
			if (resp.indexOf(clearIf) >= 0)
			{
				document.getElementById(div).innerHTML = "";
				doAfter();
			}
		}
		xmlhttp.open("POST", url , true);
		xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
		xmlhttp.send(serialized);
	}
	else
		alert("Your browser doesn't seem to support ajax");

}


//submits a page in the background
function doData(url)
{
	var XMLHTTP= XMLHttpRequest || ActiveXObject("Microsoft.XMLHTTP");
	if (typeof XMLHTTP!= "undefined" ) 
	{
		var xmlhttp = new XMLHTTP;
		xmlhttp.onreadystatechange = function() {
			var resp = xmlhttp.responseText;
		}
		xmlhttp.open("GET", url , true);
		xmlhttp.send(null);
	}
	else
		alert("Your browser doesn't seem to support ajax");
}

function cancelLogin()
{
	document.getElementById("temp").innerHTML="";
	document.getElementById("lnkLogin").setAttribute("onclick","login()");
	document.getElementById("lnkLogin").innerHTML="Login";
}

function login()
{
	loadData("temp","login.php");
	document.getElementById("lnkLogin").setAttribute("onclick","cancelLogin()");
	document.getElementById("lnkLogin").innerHTML="Cancel Login";
	//document.getElementById("submit").setAttribute("onclick", "loginSubmit()");
}

function loginSubmit()
{
	postDataLogin("login.php");	
}

function getPosts()
{
	loadData("news","getposts.php");
}


 