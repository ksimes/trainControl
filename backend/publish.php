<?php

require('./phpMQTT.php');

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: PUT, GET, POST, DELETE");
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");

$server = 'broker.mqttdashboard.com';     // change if necessary
$port = 1883;                     // change if necessary
$username = '';                   // set your username
$password = '';                   // set your password
$client_id = 'phpMQTT-publisher'; // make sure this is unique for connecting to sever - you could use uniqid()

$mqtt = new Bluerhinos\phpMQTT($server, $port, $client_id);

function executePublish($msg)
{
    global $mqtt, $username, $password;
    if ($mqtt->connect(true, NULL, $username, $password)) {
        $mqtt->publish('/simons/train', $msg, 1, false);
        echo "Msg sent " . $msg . "\n";
        $mqtt->close();
    } else {
        echo "Time out!\n";
    }
}

// Get the posted data.
$postData = file_get_contents("php://input");

if(isset($postData) && !empty($postData)) {
    echo "postData ->{$postData}";
    // Extract the data.
    $request = json_decode($postData);

    // Validate.
    if(trim($request->access) === '' || trim($request->direction) === '')
    {
        return http_response_code(400);
    }

    $access = trim($request->access);

    echo "Access ->" . $access;

    if ($access == 'faster') {
        executePublish('faster');
    } else if ($access == 'slower') {
        executePublish('slower');
    } else if ($access == 'stop') {
        executePublish('stop');
    } else if ($access == 'start') {
        executePublish('start');
    }
}

?>
