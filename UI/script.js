document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('clickMe');
    button.addEventListener('click', function() {
        fetch('http://localhost:8083/heartbeat')
            .then(response => response.json())
            .then(data => {
                console.log('Heartbeat response:', data);
                if (data.data) {
                    alert(`Blog content: ${data.data.content}`);
                } else {
                    alert('No blog data received');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error occurred. Check the console for details.');
            });
    });
});