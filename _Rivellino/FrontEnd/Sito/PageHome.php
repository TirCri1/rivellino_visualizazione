<?php
	header("Refresh: 1");
	$conn = new mysqli("localhost","root","","rivellino");
	
	if ($conn->connect_error) {
		die("Connessione fallita: ".$conn->connect_error);
	} else {
		VisTemperature();
		VisUmidita();
		VisQualitaAria();
		VisVibrazioni();
		VisAllagamento();
	}
	$conn->close();
	
	
//Funzioni
	function VisTemperature(){
		$conn = new mysqli("localhost","root","","rivellino");
		
		echo "<hr>";
		echo "<p> Dati temperature attuale: </p>";
		echo "<ul>";
		
			echo "<li> Sensore temperatura muro --- ";
				$sql = "SELECT Valore
						FROM temperatura
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
						FROM temperatura
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
						FROM temperatura
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
	
	function VisUmidita(){
		$conn = new mysqli("localhost","root","","rivellino");
		
		echo "<hr>";
		echo "<p> Dati umidità attuale: </p>";
		echo "<ul>";
		
			echo "<li> Sensore umidità muro --- ";
				$sql = "SELECT Valore
						FROM umidita
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
						FROM umidita
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
	
	function VisQualitaAria(){
		$conn = new mysqli("localhost","root","","rivellino");
		
		echo "<hr>";
		echo "<p> Dati qualita aria attuale: </p>";
		echo "<ul>";
		
			echo "<li> Sensore Co --- ";
				$sql = "SELECT ValoreCo
						FROM qualita
						WHERE NameSensore = 'SensQualitàAria1'
						ORDER BY Data DESC, Ora DESC
						LIMIT 1";
				$ris = $conn -> query($sql);
				$righe = $ris -> num_rows;
				$temp = $ris->fetch_assoc();
				if($righe==0){
					echo "Nessun dato presente";
				} else {
					echo $temp['ValoreCo']."%";
				}
			echo "</li>";
			
			echo "<li> Sensore No2 --- ";
				$sql = "SELECT ValoreNo2
						FROM qualita
						WHERE NameSensore = 'SensQualitàAria2'
						ORDER BY Data DESC, Ora DESC
						LIMIT 1";
				$ris = $conn -> query($sql);
				$righe = $ris -> num_rows;
				$temp = $ris->fetch_assoc();
				if($righe==0){
					echo "Nessun dato presente";
				} else {
					echo $temp['ValoreNo2']."%";
				}
			echo "</li>";
		
		echo "</ul>";
		$conn->close();
	}
	
	function VisVibrazioni(){
		$conn = new mysqli("localhost","root","","rivellino");
		
		echo "<hr>";
		echo "<p> Dati vibrazioni attuale: </p>";
		echo "<ul>";
		
			echo "<li> Sensore vibrazione --- ";
				$sql = "SELECT ValoreFrequenza, ValoreAmpiezza
						FROM vibrazione
						WHERE NameSensore = 'SensVibrazione'
						ORDER BY Data DESC, Ora DESC
						LIMIT 1";
				$ris = $conn -> query($sql);
				$righe = $ris -> num_rows;
				$temp = $ris->fetch_assoc();
				if($righe==0){
					echo "Nessun dato presente";
				} else {
					echo $temp['ValoreFrequenza']."Hz - ".$temp['ValoreAmpiezza']."m/s";
				}
			echo "</li>";
		
		echo "</ul>";
		$conn->close();
	}
	
	function VisAllagamento(){
		$conn = new mysqli("localhost","root","","rivellino");
		
		echo "<hr>";
		echo "<p> Dati allagamento attuale: </p>";
		echo "<ul>";
		
			echo "<li> Sensore allagamento --- ";
				$sql = "SELECT Valore
						FROM allagamento
						WHERE NameSensore = 'SensAllagamento'
						ORDER BY Data DESC, Ora DESC
						LIMIT 1";
				$ris = $conn -> query($sql);
				$righe = $ris -> num_rows;
				$temp = $ris->fetch_assoc();
				if($righe==0){
					echo "Nessun dato presente";
				} else {
					if($temp['Valore']){
						echo "E' stato rilevato un allagamento";
					} else {
						echo "La situazione allagamento è ok";
					}
				}
			echo "</li>";
		
		echo "</ul>";
		$conn->close();
	}
	
?>