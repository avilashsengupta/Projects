const current = new Date();
var objective_counter = 1;
var education_counter = 2;
var achievement_counter = 1;
var training_counter = 2;
var project_counter = 2;
var certificate_counter = 1;
var skill_counter = 2;
var interest_counter = 1;
var language_counter = 2;
function printCV()
{
	var k;
	document.getElementById('layout').style.display = 'block';
	document.getElementById('builder').style.display = 'none';
	getCVData();
	setCVData();
	k = checkUnfilledData();
	if(k == false) return;
	window.print();
	document.getElementById('layout').style.display = 'none';
	document.getElementById('builder').style.display = 'block';
}
function formatDate()
{
	var d = parseInt(current.getDate());
	var m = parseInt(current.getMonth()) + 1;
	var y = parseInt(current.getFullYear());
	var datestring = '';
	if(d <= 10) datestring += '0' + d.toString() + '/';
	else datestring += d.toString() + '/';
	if(m <= 10) datestring += '0' + m.toString() + '/';
	else datestring += m.toString() + '/';
	datestring += y.toString();
	return datestring;
}
var name, mobile, email, linkedin, github, nationality, dob, address, profile, sign, city;
function getCVData()
{
	name = document.getElementById('name_entry').value;
	mobile = document.getElementById('phone_entry').value;
	email = document.getElementById('email_entry').value;
	nationality = document.getElementById('nation_entry').value;
	dob = document.getElementById('dob_entry').value;
	address = document.getElementById('address_entry').value;
	linkedin = document.getElementById('linkedin_entry').value;
	github = document.getElementById('github_entry').value;
	profile = document.getElementById('profile_entry').value;
	sign = document.getElementById('signature_entry').value;
	city = document.getElementById('place_entry').value;
}
function setCVData()
{
	document.getElementById('name').innerHTML = name.toUpperCase();
	document.getElementById('mobile').innerHTML = mobile;
	document.getElementById('email').innerHTML = email;
	var linkedin_anchor = document.createElement('a');
	var linkedin_link = document.createTextNode(linkedin);
	linkedin_anchor.appendChild(linkedin_link)
	linkedin_anchor.href = linkedin
	document.getElementById('linkedin').appendChild(linkedin_anchor);
	var github_anchor = document.createElement('a');
	var github_link = document.createTextNode(github);
	github_anchor.appendChild(github_link)
	github_anchor.href = github
	document.getElementById('github').appendChild(github_anchor);
	document.getElementById('nation').innerHTML = nationality;
	document.getElementById('dob').innerHTML = dob;
	document.getElementById('address').innerHTML = address;
	document.getElementById('date').innerHTML = formatDate();
	document.getElementById('place').innerHTML = city;
	document.getElementById('identity').innerHTML = name;
	document.getElementById('profile').src = profile;
	document.getElementById('signature').src = sign;
}
function setCareerObjective()
{
	var text = (objective_counter).toString() + '. ' + document.getElementById('objective_entry').value;
	var tab = document.getElementById('cv_objective');
	tab.insertRow(objective_counter).insertCell(0).innerHTML = text;
	objective_counter++;
	document.getElementById('objective_entry').value = '';
}
function setEducation()
{
	var tab = document.getElementById('cv_education');
	var newrow = tab.insertRow(education_counter);
	newrow.insertCell(0).innerHTML = document.getElementById('exam_entry').value;
	newrow.insertCell(1).innerHTML = document.getElementById('year_entry').value;
	newrow.insertCell(2).innerHTML = document.getElementById('institute_entry').value;
	newrow.insertCell(3).innerHTML = document.getElementById('marks_entry').value;
	education_counter++;
	document.getElementById('exam_entry').value = '';
	document.getElementById('year_entry').value = '';
	document.getElementById('institute_entry').value = '';
	document.getElementById('marks_entry').value = '';
}
function setAchievements()
{
	var text = (achievement_counter).toString() + '. ' + document.getElementById('achievement_entry').value;
	var tab = document.getElementById('cv_achievements');
	tab.insertRow(achievement_counter).insertCell(0).innerHTML = text;
	achievement_counter++;
	document.getElementById('achievement_entry').value = '';
}
function setTrainingData()
{
	var tab = document.getElementById('cv_training');
	var newrow = tab.insertRow(training_counter);
	newrow.insertCell(0).innerHTML = document.getElementById('trainingtitle_entry').value;
	newrow.insertCell(1).innerHTML = document.getElementById('organisation_entry').value;
	newrow.insertCell(2).innerHTML = document.getElementById('location_entry').value;
	newrow.insertCell(3).innerHTML = document.getElementById('duration_entry').value;
	training_counter++;
	document.getElementById('trainingtitle_entry').value = '';
	document.getElementById('organisation_entry').value = '';
	document.getElementById('location_entry').value = '';
	document.getElementById('duration_entry').value = '';
}
function setProjectData()
{
	var tab = document.getElementById('cv_projects');
	var newrow = tab.insertRow(project_counter);
	newrow.insertCell(0).innerHTML = document.getElementById('projecttitle_entry').value;
	newrow.insertCell(1).innerHTML = document.getElementById('technology_entry').value;
	newrow.insertCell(2).innerHTML = document.getElementById('program_entry').value;
	project_counter++;
	document.getElementById('projecttitle_entry').value = '';
	document.getElementById('technology_entry').value = '';
	document.getElementById('program_entry').value = '';
}
function setCertification()
{
	var text = (certificate_counter).toString() + '. ' + document.getElementById('certificate_entry').value;
	var tab = document.getElementById('cv_certificate');
	tab.insertRow(certificate_counter).insertCell(0).innerHTML = text;
	certificate_counter++;
	document.getElementById('certificate_entry').value = '';
}
function setTechnicalSkill()
{
	var tab = document.getElementById('cv_skills');
	var newrow = tab.insertRow(skill_counter);
	newrow.insertCell(0).innerHTML = document.getElementById('skill_entry').value;
	newrow.insertCell(1).innerHTML = document.getElementById('proficiency_entry').value;
	skill_counter++;
	document.getElementById('skill_entry').value = '';
	document.getElementById('proficiency_entry').value = '';
}
function setInterestArea()
{
	var text = (interest_counter).toString() + '. ' + document.getElementById('interest_entry').value;
	var tab = document.getElementById('cv_interest');
	tab.insertRow(interest_counter).insertCell(0).innerHTML = text;
	interest_counter++;
	document.getElementById('interest_entry').value = '';
}
function setKnownLanguage()
{
	var tab = document.getElementById('cv_language');
	var newrow = tab.insertRow(language_counter);
	newrow.insertCell(0).innerHTML = document.getElementById('language_entry').value;
	newrow.insertCell(1).innerHTML = document.getElementById('read_entry').value;
	newrow.insertCell(2).innerHTML = document.getElementById('write_entry').value;
	newrow.insertCell(3).innerHTML = document.getElementById('speak_entry').value;
	language_counter++;
	document.getElementById('language_entry').value = '';
	document.getElementById('read_entry').value = '';
	document.getElementById('write_entry').value = '';
	document.getElementById('speak_entry').value = '';
}
function checkUnfilledData()
{
	if(objective_counter == 1)
	{
		window.alert('CAREER OBJECTIVE is a required field');
		return false;
	}
	if(education_counter == 2)
	{
		window.alert('EDUCATION QUALIFICATION is a required field');
		return false;
	}
	if(skill_counter == 2)
	{
		window.alert('TECHNICAL SKILLSET is a required field');
		return false;
	}
	if(interest_counter == 1)
	{
		window.alert('AREA OF INTEREST is a required field');
		return false;
	}
	if(language_counter == 2)
	{
		window.alert('LANGUAGES KNOWN is a required field');
		return false;
	}
	if(achievement_counter == 1) document.getElementById('cv_achievements').style.display = 'none';
	if(training_counter == 2) document.getElementById('cv_training').style.display = 'none';
	if(project_counter == 2) document.getElementById('cv_projects').style.display = 'none';
	if(certificate_counter == 1) document.getElementById('cv_certificate').style.display = 'none';
	return true;
}
