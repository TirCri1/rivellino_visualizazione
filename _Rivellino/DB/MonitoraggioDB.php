<?php
// Configurazione del database
$host = 'localhost';       // O il tuo host
$user = 'root';            // Il tuo username MySQL
$password = '';            // La tua password MySQL
$dbname = 'rivellino';     // Nome del tuo database

// Connessione al database
$conn = new mysqli($host, $user, $password, $dbname);

// Verifica la connessione
if ($conn->connect_error) {
    die("Connessione fallita: " . $conn->connect_error);
}

// Funzione per ottenere la configurazione principale di MySQL
function getMySQLMainConfig($conn) {
    $config = [];
    $variables = [
        'innodb_buffer_pool_size',
        'max_connections',
        'max_allowed_packet',
        'key_buffer_size',
        'wait_timeout',
        'sort_buffer_size',
        'read_buffer_size',
        'read_rnd_buffer_size',
        'thread_cache_size',
        'table_open_cache',
        'tmp_table_size',
        'max_heap_table_size',
        'innodb_log_file_size'
    ];

    foreach ($variables as $variable) {
        $query = "SHOW VARIABLES LIKE '$variable'";
        $result = $conn->query($query);
        if ($result) {
            $config[] = $result->fetch_assoc();
        } else {
            die("Errore durante la query: " . $conn->error);
        }
    }
    return $config;
}

// Funzione per formattare i valori in MB o GB, se applicabile
function formatSize($size) {
    if ($size >= 1073741824) {
        return round($size / 1073741824, 2) . ' GB';
    }
    if ($size >= 1048576) {
        return round($size / 1048576, 2) . ' MB';
    }
    return $size . ' B';
}

// Funzione per ottenere le informazioni sulle connessioni attive
function getConnectionsStatus($conn) {
    $query = "SHOW STATUS LIKE 'Threads_connected'";
    $result = $conn->query($query);
    if ($result) {
        return $result->fetch_assoc()['Value'];
    } else {
        return "Errore durante il recupero dello stato delle connessioni.";
    }
}

// Funzione per ottenere lo stato delle transazioni
function getTransactionStatus($conn) {
    $query = "SHOW ENGINE INNODB STATUS";
    $result = $conn->query($query);

    if ($result) {
        $row = $result->fetch_assoc();
        $status = $row['Status'];

        if (strpos($status, 'TRANSACTIONS') !== false) {
            return "Ci sono transazioni in corso.";
        } else {
            return "Nessuna transazione bloccata o in sospeso.";
        }
    } else {
        return "Impossibile ottenere lo stato delle transazioni.";
    }
}

// Funzione per ottenere le dimensioni del database e delle tabelle
function getDatabaseSize($conn, $dbname) {
    $query = "SELECT table_name, 
                 ROUND((data_length + index_length) / 1024 / 1024, 2) AS 'Size_MB',
                 table_rows 
              FROM information_schema.tables
              WHERE table_schema = ?";

    $stmt = $conn->prepare($query);
    if ($stmt === false) {
        die("Errore nella preparazione della query: " . $conn->error);
    }
    $stmt->bind_param("s", $dbname);
    $stmt->execute();
    $result = $stmt->get_result();

    $data = [];
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }

    return $data;
}

// Cattura i dati delle tabelle per il grafico
function getTableData($conn, $dbname) {
    $tables = getDatabaseSize($conn, $dbname);
    $tableNames = [];
    $tableSizes = [];
    foreach ($tables as $table) {
        $tableNames[] = $table['table_name'];
        $tableSizes[] = (float) $table['Size_MB'];
    }
    return ['labels' => $tableNames, 'data' => $tableSizes];
}
?>



<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitoraggio Database Rivellino</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        h1 {
            color: #333;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
        }
        .chart-container {
            width: 48%;
            margin-bottom: 20px;
        }

        /* Aggiungere larghezza ai grafici delle tabelle */
        #tableChart {
            max-width: 100%;
            max-height: 400px;
            width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <h1>Monitoraggio Database Rivellino</h1>

    <div class="container">
        <div class="chart-container">
            <h2>Grafico delle Dimensioni delle Tabelle</h2>
            <canvas id="tableChart"></canvas>
        </div>

        <div class="chart-container">
            <h2>Configurazione MySQL/MariaDB</h2>
            <table>
                <tr>
                    <th>Variabile</th>
                    <th>Valore</th>
                    <th>Descrizione</th>
                </tr>
                <?php
                    $config = getMySQLMainConfig($conn);
                    foreach ($config as $row) {
                        $value = $row['Value'];
                        if (is_numeric($value)) {
                            $value = formatSize($value);
                        }

                        $description = '';
                        switch ($row['Variable_name']) {
                            case 'innodb_buffer_pool_size':
                                $description = 'Dimensione della memoria utilizzata per memorizzare i dati InnoDB.';
                                break;
                            case 'max_connections':
                                $description = 'Numero massimo di connessioni simultanee al database.';
                                break;
                            case 'max_allowed_packet':
                                $description = 'Dimensione massima per un pacchetto di dati che può essere inviato o ricevuto dal server MySQL.';
                                break;
                            case 'key_buffer_size':
                                $description = 'Dimensione della memoria cache per gli indici delle tabelle MyISAM.';
                                break;
                            case 'wait_timeout':
                                $description = 'Numero di secondi che il server MySQL aspetta prima di terminare una connessione inattiva.';
                                break;
                            case 'sort_buffer_size':
                                $description = 'Dimensione della memoria utilizzata per operazioni di ordinamento.';
                                break;
                            case 'read_buffer_size':
                                $description = 'Dimensione del buffer di lettura per operazioni di scansione sequenziale.';
                                break;
                            case 'read_rnd_buffer_size':
                                $description = 'Dimensione del buffer di lettura per operazioni di lettura casuale.';
                                break;
                            case 'thread_cache_size':
                                $description = 'Numero di thread che MySQL tiene in cache per gestire le connessioni.';
                                break;
                            case 'table_open_cache':
                                $description = 'Numero di tabelle che MySQL tiene aperte simultaneamente.';
                                break;
                            case 'tmp_table_size':
                                $description = 'Dimensione massima di una tabella temporanea in memoria.';
                                break;
                            case 'max_heap_table_size':
                                $description = 'Dimensione massima di una tabella in memoria (heap).';
                                break;
                            case 'innodb_log_file_size':
                                $description = 'Dimensione dei file di log di InnoDB.';
                                break;
                        }

                        echo "<tr>
                                <td>" . $row['Variable_name'] . "</td>
                                <td>" . $value . "</td>
                                <td>" . $description . "</td>
                              </tr>";
                    }
                ?>
            </table>
        </div>
    </div>

    <h2>Connessioni attive</h2>
    <p>Connessioni attuali: <?php echo getConnectionsStatus($conn); ?></p>

    <h2>Stato delle Transazioni</h2>
    <p><?php echo getTransactionStatus($conn); ?></p>

    <h2>Dimensione delle tabelle</h2>
    <table id="tables-data">
        <tr>
            <th>Tabella</th>
            <th>Dimensione (MB)</th>
            <th>Numero di righe</th>
        </tr>
        <?php
            $tables = getDatabaseSize($conn, $dbname);
            foreach ($tables as $table) {
                echo "<tr>
                        <td>" . $table['table_name'] . "</td>
                        <td>" . $table['Size_MB'] . " MB</td>
                        <td>" . $table['table_rows'] . "</td>
                      </tr>";
            }
        ?>
    </table>



    <script>
        let tableChart;

            // Grafico Dimensione Tabelle
            const tableData = <?php echo json_encode(getTableData($conn, $dbname)); ?>;
            const ctxTable = document.getElementById('tableChart').getContext('2d');
            tableChart = new Chart(ctxTable, {
                type: 'bar',
                data: {
                    labels: tableData.labels,
                    datasets: [{
                        label: 'Dimensione (MB)',
                        data: tableData.data,
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: { scales: { y: { beginAtZero: true } } }
            });
        }

        updateSystemCharts();
        setInterval(() => location.reload(), 10000); // Ricarica ogni 10 sec per aggiornare i valori
    </script>
</body>
</html>