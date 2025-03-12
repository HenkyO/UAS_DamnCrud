<?php

function pdo_connect(){
    $DATABASE_HOST = 'uas-db';
    $DATABASE_USER = 'root';
    $DATABASE_PASS = 'useruas';
    $DATABASE_NAME = 'damncrud';
    try {
        $pdo = new PDO("mysql:host=$DATABASE_HOST;dbname=$DATABASE_NAME;charset=utf8", $DATABASE_USER, $DATABASE_PASS);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        return $pdo;
    } catch (PDOException $exception) {
        die ('Failed to connect to database! ' . $exception->getMessage());
    }
}

function style_script(){
    return '
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap4.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min.js"></script>   
    <script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap4.min.js"></script>';
}