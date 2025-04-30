<?php
	// casa: https://192.168.1.118
	// scuola: https://10.10.60.186

	$azione = $_POST['action'];

	if ($azione === 'login') {
		$utente = $_POST['user'];
		$password = $_POST['pw'];
		$conn = new mysqli("localhost", "root", "", "rivellino");
		
		if ($conn->connect_error) {
			die("Connessione fallita: " . $conn->connect_error);
			header("Refresh: 5; url=https://10.10.60.186");
			exit();
		}

		$sql = "SELECT passwordUtente FROM Utente WHERE userUtente = ?";
		$stmt = $conn->prepare($sql);
		$stmt->bind_param("s", $utente);
		$stmt->execute();
		$ris = $stmt->get_result();

		if ($ris->num_rows == 0) {
			echo "Utente inesistente!";
			header("Refresh: 5; url=https://10.10.60.186");
			exit();
		} else {
			$pwUtente = $ris->fetch_assoc();
			if (password_verify($password, $pwUtente['passwordUtente'])) {
				echo "Accesso eseguito con successo!";
				header("Refresh: 3; url=https://10.10.60.186/_Rivellino/FrontEnd/Sito/PageHome.php");
				exit();
			} else {
				echo "Password errata!";
				header("Refresh: 5; url=https://10.10.60.186");
				exit();
			}
		}
		
		$stmt->close();
		$conn->close();
		
	} else {
		echo "Azione sconosciuta!";
		header("Refresh: 5; url=https://10.10.60.186");
		exit();
	}
	
?>
