<?php
$player = $_REQUEST['From'];
$body = $_REQUEST['Body'];
if(!file_exists('players')) mkdir('players', 0777);
$players  = json_decode(file_get_contents("players/players.json"));
if (is_null($players)) $players = [];
$json_obj = null;
if(!player_exists($player,$players)){
	$json_obj = generate_quote($player);
	$res = $json_obj->body;
		
}else{
	$res = check_answer();
}
$json_write= json_encode($players);
file_put_contents("players/players.json", $json_write);
function player_exists($player,$players){
	return array_key_exists($player,$players);
}
function generate_quote($player){
	$choices = ['Jaden','Trump'];
	$choice = $choices[array_rand($choices)];
	$players[$player] = $choice;
	return  json_decode(exec('python quote.py '.$choice));
}
function check_answer($player){
	if($body == $players[$player] ){
		
		$return =  "Correct";
	}
	else{
		$return = "Incorrect";
	}
	unset($players[$player]);
	return $return;
}
?>
<Response>
	<Message><?php echo $res?> </Message>
</Response>
