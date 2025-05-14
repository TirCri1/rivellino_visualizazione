<?php
	$servername = "localhost";
	$username = "root";
	$password = "";
	$dbname = "rivellino";

	$conn = new mysqli($servername, $username, $password, $dbname);
	if ($conn->connect_error) {
		die("Connessione fallita: " . $conn->connect_error);
	}

	// Dati dell'utente
	$user = "admin";  // Cambia con il nome utente che vuoi inserire
	$password_pulita = "admin";  // Cambia con la password dell'utente


	$password_hash = password_hash($password_pulita, PASSWORD_DEFAULT);

	$sql = "INSERT INTO Utente (userUtente, passwordUtente) VALUES (?, ?)";

	$stmt = $conn->prepare($sql);
	$stmt->bind_param("ss", $user, $password_hash);

	if ($stmt->execute()) {
		echo "Utente registrato con successo! <br>";
		echo "User: ".$user."<br>";
		echo "Password: ".$password_pulita."<br>" ;
		echo "Password segreta: ".$password_hash ;
	} else {
		echo "Errore durante la registrazione: " . $stmt->error;
	}

	$stmt->close();
	$conn->close();
?>
