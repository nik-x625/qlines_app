$(document).ready(function () {
    $('#data').DataTable({
        ajax: '/api/data',
        serverSide: true,
        columns: [
            { data: 'user_name' },
            { data: 'client_name' },
            { data: 'first_message' },
            { data: 'last_message' }
        ],
        order: [[3,'desc']]
    });
});
