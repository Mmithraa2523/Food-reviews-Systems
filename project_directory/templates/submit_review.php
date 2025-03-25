<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $reviewer = $_POST['reviewer'];
    $email = $_POST['email'];
    $date = $_POST['date'];
    $rating = $_POST['rating'];
    $review = $_POST['review'];
    $restaurant = $_GET['restaurant']; // Get restaurant name from URL

    // Connect to MySQL database
    $mysqli = new mysqli("localhost", "username", "password", "database_name");

    // Check connection
    if ($mysqli->connect_error) {
        die("Connection failed: " . $mysqli->connect_error);
    }

    // Prepare SQL query to insert the review
    $stmt = $mysqli->prepare("INSERT INTO reviews (restaurant, reviewer, email, date, rating, review) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("ssssds", $restaurant, $reviewer, $email, $date, $rating, $review);
    
    if ($stmt->execute()) {
        echo "Review submitted successfully!";
    } else {
        echo "Error: " . $stmt->error;
    }

    // Close the connection
    $stmt->close();
    $mysqli->close();
}
?>
