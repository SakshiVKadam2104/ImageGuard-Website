<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];

    // Validate the username and password (You should use a more secure method)
    if ($username === "your_username" && $password === "your_password") {
        // Successful login, you can redirect to a dashboard or other page
        header("Location: dashboard.php");
        exit();
    } else {
        echo "Invalid username or password. Please try again.";
    }
}
?>
