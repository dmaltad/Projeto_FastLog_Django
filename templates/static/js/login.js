// Dados de exemplo para simular um banco de dados
const usuarios = [
    { email: 'admin@dominio.com', password: 'admin', userType: 'admin' },
    { email: 'cliente@empresa.com', password: 'cliente123', userType: 'cliente' }
];

document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const emailInput = document.getElementById('email').value;
    const passwordInput = document.getElementById('password').value;
    const errorMessageDiv = document.getElementById('error-message');

    // Procura por um usuário com as credenciais inseridas
    const usuarioAutenticado = usuarios.find(user =>
        user.email === emailInput && user.password === passwordInput
    );

    if (usuarioAutenticado) {
        // Credenciais válidas, redireciona com base no tipo de usuário
        if (usuarioAutenticado.userType === 'admin') {
            window.location.href = 'admin-dashboard.html';
        } else if (usuarioAutenticado.userType === 'cliente') {
            window.location.href = 'cliente-painel.html';
        }
    } else {
        // Credenciais inválidas, exibe mensagem de erro
        errorMessageDiv.textContent = 'Credenciais inválidas. Por favor, tente novamente.';
        errorMessageDiv.style.display = 'block';
    }
});
