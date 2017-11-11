<?php

$domain = $_POST['domain'];
$subDomain = $_POST['subdomain'];
$phoneNoForCall = $_POST['phonecellno'];
$phoneCondition = $_POST['call_state'];
$emailID = $_POST['emailid'];
$emailBody = $_POST['emailbody'];
$emailCondition = $_POST['email_state'];
$phoneNoForSMS = $_POST['cellno'];
$messageBody = $_POST['msgbody'];
$smsCondition = $_POST['sms_state'];
$service = array("call", "sms", "email");
$noOfService = 0;
foreach ($service as $serve)
{
    $noOfService++;
}

$serviceJson = array(
    array('Service_name' => $service[0],
        'Service_info' => array($phoneNoForCall),
        'Conditional_keywords' => $phoneCondition),
    array('Service_name' => $service[1],
        'Service_info' => array($emailID, $emailBody),
        'Conditional_keywords' => $smsCondition),
    array('Service_name' => $service[2],
        'Service_info' => array($phoneNoForSMS, $messageBody),
        'Conditional_keywords' => $emailCondition));

$fulljson = array(
    'User_id' => '1',
    'Domain' => array($domain,$subDomain),
    'Number_of_sensor' => '1',
    'Sensor_name' => array('pulse rate'),
    'Number_of_service' => $noOfService,
    'Services' => $serviceJson);


$fileName = '../watch/user_intention.json';
$filePointer = fopen($fileName, "wb") or die('Cannot open file:  ' . $fileName);
fwrite($filePointer, json_encode($fulljson));
fclose($filePointer);


echo "<br><h1 style='color: green' align='center'>User intention generated Successfully!!</h1><br>";

?>

<html>
<head>
    <link rel="stylesheet" type="text/css" href="assets/css/bootstrap.css"/>
</head>
<div>
    <button class="btn btn-success btn-block" onclick="document.location.href='/index.html'">Home/Again</button>
</div>
</html>
