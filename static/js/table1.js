$(document).ready(function () {
    $('#data').DataTable({
        ajax: '/api/data',
        serverSide: true,
        columns: [
            { data: 'user_name' },
            { data: 'client_name' },
            { data: 'last_message' },
            { data: 'first_message' }
        ],
    });
});
