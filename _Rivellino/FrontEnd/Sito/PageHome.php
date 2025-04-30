<?php
	header("Refresh: 10");
	$conn = new mysqli("localhost","root","","rivellino");
	
	if ($conn->connect_error) {
		die("Connessione fallita: " . $conn->connect_error);
	} else {
		StampaTemperature();
		StampaUmidita();
	}
	$conn->close();
	
	
//Funzioni
	function StampaTemperature(){
		$conn = new mysqli("localhost","root","","rivellino");
		
		echo "<hr>";
		echo "<p> Dati temperature attuale: </p>";
		echo "<ul>";
		
		echo "<li> Sensore temperatura muro --- ";
		$sql = "SELECT Valore
				FROM Temperatura
				WHERE NameSensore = 'SensTemp1'
				ORDER BY Data DESC, Ora DESC
				LIMIT 1";
		$ris = $conn -> query($sql);
		$righe = $ris -> num_rows;
		$temp = $ris->fetch_assoc();
		if($righe==0){
			echo "Nessun dato presente";
		} else {
			echo $temp['Valore']."°C";
		}
		echo "</li>";
		
		echo "<li> Sensore temperatura polveriera --- ";
		$sql = "SELECT Valore
				FROM Temperatura
				WHERE NameSensore = 'SensTemp2'
				ORDER BY Data DESC, Ora DESC
				LIMIT 1";
		$ris = $conn -> query($sql);
		$righe = $ris -> num_rows;
		$temp = $ris->fetch_assoc();
		if($righe==0){
			echo "Nessun dato presente";
		} else {
			echo $temp['Valore']."°C";
		}
		echo "</li>";
		
		echo "<li> Sensore temperatura galleria --- ";
		$sql = "SELECT Valore
				FROM Temperatura
				WHERE NameSensore = 'SensTemp3'
				ORDER BY Data DESC, Ora DESC
				LIMIT 1";
		$ris = $conn -> query($sql);
		$righe = $ris -> num_rows;
		$temp = $ris->fetch_assoc();
		if($righe==0){
			echo "Nessun dato presente";
		} else {
			echo $temp['Valore']."°C";
		}
		echo "</li>";
		
		echo "</ul>";
		$conn->close();
	}
	
	function StampaUmidita(){
		$conn = new mysqli("localhost","root","","rivellino");
		
		echo "<hr>";
		echo "<p> Dati umidità attuale: </p>";
		echo "<ul>";
		
		echo "<li> Sensore umidità muro --- ";
		$sql = "SELECT Valore
				FROM Umidita
				WHERE NameSensore = 'SensUmid1'
				ORDER BY Data DESC, Ora DESC
				LIMIT 1";
		$ris = $conn -> query($sql);
		$righe = $ris -> num_rows;
		$temp = $ris->fetch_assoc();
		if($righe==0){
			echo "Nessun dato presente";
		} else {
			echo $temp['Valore']."%";
		}
		echo "</li>";
		
		echo "<li> Sensore umidità polveriera --- ";
		$sql = "SELECT Valore
				FROM umidita
				WHERE NameSensore = 'SensUmid2'
				ORDER BY Data DESC, Ora DESC
				LIMIT 1";
		$ris = $conn -> query($sql);
		$righe = $ris -> num_rows;
		$temp = $ris->fetch_assoc();
		if($righe==0){
			echo "Nessun dato presente";
		} else {
			echo $temp['Valore']."%";
		}
		echo "</li>";
		
		echo "<li> Sensore umidità galleria --- ";
		$sql = "SELECT Valore
				FROM Umidita
				WHERE NameSensore = 'SensUmid3'
				ORDER BY Data DESC, Ora DESC
				LIMIT 1";
		$ris = $conn -> query($sql);
		$righe = $ris -> num_rows;
		$temp = $ris->fetch_assoc();
		if($righe==0){
			echo "Nessun dato presente";
		} else {
			echo $temp['Valore']."%";
		}
		echo "</li>";
		
		echo "</ul>";
		$conn->close();
	}
?>