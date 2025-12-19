<?php

if (!isset($_SESSION)) {
    session_start();
}
$db = mysqli_connect('127.0.0.1', 'admin', '1234', 'newtest');

if (!$db) {
    die(mysqli_connect_error());
}
$db->query('SET NAMES UTF8');

function ex($data, $s = ' , ', $c = ' = ')
{
    global $db;
    $array = [];
    if (is_array($data)) {
        foreach ($data as $k => $v) {
            $v = htmlspecialchars($db->real_escape_string($v));
            $array[] = "`$k`$c'$v'";
        }
    } else {
        $array[] = $data;
    }
    $array = join($s, $array);
    return $array;
}
function sel($table, $where = 1)
{
    global $db;
    $w = ex($where, " AND ");
    $sql = "SELECT * FROM `$table` WHERE $w";
    $res = $db->query($sql);
    return $res->fetch_assoc();
}
function sels($table, $where = 1, $other = '', $method = 'equa', $dd = false)
{
    global $db;
    $w = '';
    if ($method == 'equa') {
        $w = ex($where, " AND ");
    } else {
        $w = ex($where, " OR ", " LIKE ");
    }
    $sql = "SELECT * FROM `$table` WHERE $w " . $other;
    if ($dd) {
        dd($sql);
    }
    $res = $db->query($sql);
    $array = [];
    while ($r = $res->fetch_assoc()) {
        $array[] = $r;
    }
    return $array;
}
function ins($table, $data)
{
    global $db;
    $d = ex($data);
    $sql = "INSERT INTO `$table` SET $d";
    $db->query($sql);
    return $db->insert_id;
}
function upd($table, $data, $where)
{
    global $db;
    $d = ex($data);
    $w = ex($where, " AND ");
    $sql = "UPDATE `$table` SET $d WHERE $w";
    $db->query($sql);
}
function del($table, $where)
{
    global $db;
    $w = ex($where, " AND ");
    $sql = "DELETE FROM `$table` WHERE $w";
    $db->query($sql);
}
function dd($data)
{
    echo "<pre>";
    var_dump($data);
    echo "</pre>";
    die();
}
function alert($msg, $l = '')
{
    echo "<script>alert('$msg');location.href = '$l'</script>";
    die();
}
function location($href = '')
{
    echo "<script>location.href = '$href'</script>";
    die;
}
