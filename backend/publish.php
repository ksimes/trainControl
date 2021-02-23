<?php

require('./phpMQTT.php');

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

if ($_POST['action'] == 'faster') {
    executePublish('faster');
} else if ($_POST['action'] == 'slower') {
    executePublish('slower');
    } else if ($_POST['action'] == 'stop') {
    executePublish('stop');
    } else if ($_POST['action'] == 'start') {
    executePublish('start');
    }

?>
