const accessToken = localStorage.getItem('access_token');

if (accessToken) {
  fetch('/accounts/api/token/verify/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + accessToken
    },
    body: JSON.stringify({ token: accessToken })
  })
  .then(res => {
    if (res.ok) {
      // Redirect to dashboard if token is valid
      window.location.href = "/dashboard/";
    } else {
      console.error("Token verification failed:", res.status);
      // Stay on the home page if token is invalid
    }
  })
  .catch(err => {
    console.error("Error verifying token:", err);
    // Stay on the home page on error
  });
} else {
  // Stay on the home page if no token is found
}
