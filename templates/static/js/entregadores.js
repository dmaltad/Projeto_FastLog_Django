// Funcionalidade de Busca e Filtros
const searchInput = document.getElementById('searchInput');
const statusFilters = document.getElementById('status-filters');
const entregadoresTableBody = document.getElementById('entregadoresTableBody');
const allTableRows = entregadoresTableBody.querySelectorAll('tr');

// Lógica de busca
searchInput.addEventListener('input', (event) => {
    const searchTerm = event.target.value.toLowerCase();
    allTableRows.forEach(row => {
        const rowText = row.innerText.toLowerCase();
        if (rowText.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Lógica de filtro por status
statusFilters.addEventListener('click', (event) => {
    event.preventDefault();
    const clickedLink = event.target.closest('a.nav-link');
    if (!clickedLink) return;

    // Remove a classe 'active' de todos e adiciona ao clicado
    statusFilters.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    clickedLink.classList.add('active');

    const status = clickedLink.dataset.status;

    allTableRows.forEach(row => {
        const rowStatus = row.dataset.status;
        if (status === 'Todos' || rowStatus === status) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Modal de visualizar/editar/deletar
const viewEditModal = new bootstrap.Modal(document.getElementById('viewEditEntregadorModal'));
const deleteModal = new bootstrap.Modal(document.getElementById('deleteEntregadorModal'));
let selectedRow = null;

document.getElementById('entregadoresTableBody').addEventListener('click', (event) => {
    const clickedButton = event.target.closest('a');
    if (!clickedButton) return;

    const row = clickedButton.closest('tr');
    selectedRow = row;

    const nome = row.dataset.nome;
    const telefone = row.dataset.telefone;
    const endereco = row.dataset.endereco;
    const documento = row.dataset.documento;
    const placa = row.dataset.placa;
    const status = row.dataset.status;

    const viewEditModalLabel = document.getElementById('viewEditEntregadorModalLabel');
    const saveEditBtn = document.getElementById('saveEditBtn');
    const formFields = document.querySelectorAll('#viewEditForm input, #viewEditForm select');

    if (clickedButton.classList.contains('visualize-btn')) {
        viewEditModalLabel.textContent = 'Ver Detalhes do Entregador';
        saveEditBtn.classList.add('d-none');
        formFields.forEach(field => field.readOnly = true);
        document.getElementById('viewEditStatus').disabled = true;

    } else if (clickedButton.classList.contains('edit-btn')) {
        viewEditModalLabel.textContent = 'Editar Entregador';
        saveEditBtn.classList.remove('d-none');
        formFields.forEach(field => field.readOnly = false);
        document.getElementById('viewEditStatus').disabled = false;

    } else if (clickedButton.classList.contains('delete-btn')) {
        document.getElementById('courierNameToDelete').textContent = nome;
        deleteModal.show();
        return;
    }

    // Preenche os campos do modal
    document.getElementById('viewEditNome').value = nome;
    document.getElementById('viewEditTelefone').value = telefone;
    document.getElementById('viewEditEndereco').value = endereco;
    document.getElementById('viewEditDocumento').value = documento;
    document.getElementById('viewEditPlaca').value = placa;
    document.getElementById('viewEditStatus').value = status;
});

// Lógica para o botão de apagar
document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
    if (selectedRow) {
        selectedRow.remove();
        deleteModal.hide();
    }
});

// Lógica para o botão de editar (salvar alterações)
document.getElementById('saveEditBtn').addEventListener('click', () => {
    if (selectedRow) {
        const nome = document.getElementById('viewEditNome').value;
        const telefone = document.getElementById('viewEditTelefone').value;
        const endereco = document.getElementById('viewEditEndereco').value;
        const documento = document.getElementById('viewEditDocumento').value;
        const placa = document.getElementById('viewEditPlaca').value;
        const status = document.getElementById('viewEditStatus').value;

        // Atualiza a linha da tabela
        selectedRow.dataset.nome = nome;
        selectedRow.dataset.telefone = telefone;
        selectedRow.dataset.endereco = endereco;
        selectedRow.dataset.documento = documento;
        selectedRow.dataset.placa = placa;
        selectedRow.dataset.status = status;

        selectedRow.cells[1].textContent = nome;
        selectedRow.cells[2].textContent = telefone;
        selectedRow.cells[3].innerHTML = `<span class="badge badge-status rounded-pill text-bg-${status === 'Ativo' ? 'success' : 'danger'}">${status}</span>`;

        viewEditModal.hide();
    }
});

// Preview da imagem no modal (adicionei no modal de adicionar também)
document.getElementById('entregadorFoto').addEventListener('change', function (event) {
    const [file] = event.target.files;
    if (file) {
        document.querySelector('#novoEntregadorModal .img-preview').src = URL.createObjectURL(file);
    }
});
