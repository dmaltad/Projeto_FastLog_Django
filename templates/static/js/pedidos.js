// Funcionalidade de Busca e Filtros
const searchInput = document.getElementById('searchInput');
const statusFilters = document.getElementById('status-filters');
const pedidosTableBody = document.getElementById('pedidosTableBody');
const allTableRows = pedidosTableBody.querySelectorAll('tr');

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

// Lógica do modal de Novo Pedido
const addItemBtn = document.getElementById('addItemBtn');
const itensPedidoContainer = document.getElementById('itensPedidoContainer');
const taxaEntregaInput = document.getElementById('taxaEntrega');

addItemBtn.addEventListener('click', () => {
    const newItemRow = document.createElement('div');
    newItemRow.className = 'col-12 mb-3 item-pedido-row';
    newItemRow.innerHTML = `
                <div class="row g-2 align-items-end">
                    <div class="col-md-5">
                        <label for="itemNome" class="form-label">Item</label>
                        <input type="text" class="form-control item-input-field" id="itemNome">
                    </div>
                    <div class="col-md-2">
                        <label for="itemQuantidade" class="form-label">Quantidade</label>
                        <input type="number" class="form-control item-input-field" id="itemQuantidade" min="1" value="1">
                    </div>
                    <div class="col-md-3">
                        <label for="itemPreco" class="form-label">Preço Unitário</label>
                        <div class="input-group">
                            <span class="input-group-text">R$</span>
                            <input type="number" class="form-control item-input-field" id="itemPreco" step="0.01" min="0">
                        </div>
                    </div>
                    <div class="col-md-2 d-flex align-items-end">
                        <button type="button" class="btn btn-danger w-100 delete-item-btn"><i class="fas fa-trash-alt"></i></button>
                    </div>
                </div>
            `;
    itensPedidoContainer.appendChild(newItemRow);
});

itensPedidoContainer.addEventListener('click', (event) => {
    if (event.target.classList.contains('delete-item-btn') || event.target.parentElement.classList.contains('delete-item-btn')) {
        const rowToRemove = event.target.closest('.item-pedido-row');
        if (rowToRemove) {
            rowToRemove.remove();
            calculateTotal('novoPedido');
        }
    }
});

const subtotalSpan = document.getElementById('subtotal');
const valorTotalPedidoSpan = document.getElementById('valorTotalPedido');

function calculateTotal(modalId) {
    let subtotal = 0;
    let container;
    if (modalId === 'novoPedido') {
        container = itensPedidoContainer;
    } else if (modalId === 'viewEditPedido') {
        container = document.getElementById('viewEditItensContainer');
    }

    const itemRows = container.querySelectorAll('.item-pedido-row');
    itemRows.forEach(row => {
        const quantidade = parseFloat(row.querySelector('input[type="number"]').value) || 0;
        const preco = parseFloat(row.querySelector('input[type="number"][step="0.01"]').value) || 0;
        subtotal += quantidade * preco;
    });

    let taxaEntrega = 0;
    if (modalId === 'novoPedido') {
        taxaEntrega = parseFloat(taxaEntregaInput.value) || 0;
    } else if (modalId === 'viewEditPedido') {
        taxaEntrega = parseFloat(document.getElementById('viewEditTaxaEntrega').value) || 0;
    }

    const valorTotal = subtotal + taxaEntrega;

    if (modalId === 'novoPedido') {
        subtotalSpan.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
        valorTotalPedidoSpan.textContent = `R$ ${valorTotal.toFixed(2).replace('.', ',')}`;
    } else {
        document.getElementById('viewEditSubtotal').textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
        document.getElementById('viewEditValorTotal').textContent = `R$ ${valorTotal.toFixed(2).replace('.', ',')}`;
    }
}

itensPedidoContainer.addEventListener('input', (event) => {
    if (event.target.classList.contains('item-input-field')) {
        calculateTotal('novoPedido');
    }
});

taxaEntregaInput.addEventListener('input', () => calculateTotal('novoPedido'));

// Lógica dos botões de Visualizar, Editar e Apagar
const viewEditModal = new bootstrap.Modal(document.getElementById('viewEditPedidoModal'));
const deleteModal = new bootstrap.Modal(document.getElementById('deletePedidoModal'));
let selectedRow = null;

// CORREÇÃO: Gerenciamento manual da barra de rolagem
// Oculta a barra de rolagem do body quando o modal é exibido
document.getElementById('viewEditPedidoModal').addEventListener('show.bs.modal', function () {
    document.body.style.overflow = 'hidden';
});

// Restaura a barra de rolagem do body quando o modal é fechado
document.getElementById('viewEditPedidoModal').addEventListener('hidden.bs.modal', function () {
    document.body.style.overflow = 'auto';
});

document.getElementById('pedidosTableBody').addEventListener('click', (event) => {
    const clickedButton = event.target.closest('a');
    if (!clickedButton) return;

    const row = clickedButton.closest('tr');
    selectedRow = row;

    const data = selectedRow.dataset;
    const formasPagamento = data.formasPagamento ? data.formasPagamento.split(',') : [];
    const itens = JSON.parse(data.itens);

    const viewEditModalLabel = document.getElementById('viewEditPedidoModalLabel');
    const saveEditBtn = document.getElementById('saveEditBtn');
    const itensContainer = document.getElementById('viewEditItensContainer');
    itensContainer.innerHTML = '';
    
    // Habilitar/Desabilitar todos os campos do modal
    function toggleFields(enable) {
        document.querySelectorAll('#viewEditForm input, #viewEditForm select, #viewEditForm textarea').forEach(field => {
            field.readOnly = !enable;
            field.disabled = !enable;
        });
        document.getElementById('viewEditEntregadorAtribuido').disabled = !enable;
        document.getElementById('viewEditPedidoStatus').disabled = !enable;
        document.querySelectorAll('#viewEditForm input[name="viewEditFormaPagamento"]').forEach(checkbox => checkbox.disabled = !enable);
        document.getElementById('viewEditPagoCheckbox').disabled = !enable;
        
        // Habilitar/Desabilitar botões de exclusão de item
        itensContainer.querySelectorAll('.delete-item-btn').forEach(btn => {
            btn.style.display = enable ? '' : 'none';
        });
    }

    if (clickedButton.classList.contains('visualize-btn')) {
        viewEditModalLabel.textContent = 'Ver Detalhes do Pedido';
        saveEditBtn.classList.add('d-none');
        toggleFields(false); // Desabilita todos os campos para visualização
        
    } else if (clickedButton.classList.contains('edit-btn')) {
        viewEditModalLabel.textContent = 'Editar Pedido';
        saveEditBtn.classList.remove('d-none');
        toggleFields(true); // Habilita todos os campos para edição
        
    } else if (clickedButton.classList.contains('delete-btn')) {
        document.getElementById('pedidoIdToDelete').textContent = data.id;
        deleteModal.show();
        return;
    } else if (clickedButton.classList.contains('print-btn')) {
        printOrder(row);
        return;
    }

    // Preenche os campos estáticos do modal
    document.getElementById('viewEditNomeCliente').value = data.cliente;
    document.getElementById('viewEditTelefoneContato').value = data.telefone;
    document.getElementById('viewEditEnderecoEntrega').value = data.endereco;
    document.getElementById('viewEditObservacoes').value = data.observacoes;
    document.getElementById('viewEditEntregadorAtribuido').value = data.entregador;
    document.getElementById('viewEditPedidoStatus').value = data.status;
    document.getElementById('viewEditTaxaEntrega').value = parseFloat(data.taxa);
    document.getElementById('viewEditPagoCheckbox').checked = data.pago === "Sim";

    // Preenche as formas de pagamento
    document.querySelectorAll('#viewEditForm input[name="viewEditFormaPagamento"]').forEach(checkbox => {
        checkbox.checked = formasPagamento.includes(checkbox.value);
    });

    // Preenche os itens dinamicamente
    itens.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'col-12 mb-3 item-pedido-row';
        itemDiv.innerHTML = `
                    <div class="row g-2 align-items-end">
                        <div class="col-md-5">
                            <label class="form-label">Item</label>
                            <input type="text" class="form-control item-input-field" value="${item.nome}">
                        </div>
                        <div class="col-md-2">
                            <label class="form-label">Quantidade</label>
                            <input type="number" class="form-control item-input-field" min="1" value="${item.quantidade}">
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Preço Unitário</label>
                            <div class="input-group">
                                <span class="input-group-text">R$</span>
                                <input type="number" class="form-control item-input-field" step="0.01" min="0" value="${item.preco}">
                            </div>
                        </div>
                        <div class="col-md-2 d-flex align-items-end">
                            <button type="button" class="btn btn-danger w-100 delete-item-btn"><i class="fas fa-trash-alt"></i></button>
                        </div>
                    </div>
                `;
        itensContainer.appendChild(itemDiv);
    });

    calculateTotal('viewEditPedido');

    // Re-adiciona os listeners para os campos do modal
    const viewEditTaxaEntregaInput = document.getElementById('viewEditTaxaEntrega');
    viewEditTaxaEntregaInput.addEventListener('input', () => calculateTotal('viewEditPedido'));
    itensContainer.addEventListener('input', (event) => {
        if (event.target.classList.contains('item-input-field')) {
            calculateTotal('viewEditPedido');
        }
    });
    itensContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-item-btn') || event.target.parentElement.classList.contains('delete-item-btn')) {
            const rowToRemove = event.target.closest('.item-pedido-row');
            if (rowToRemove) {
                rowToRemove.remove();
                calculateTotal('viewEditPedido');
            }
        }
    });
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
        const novoStatus = document.getElementById('viewEditPedidoStatus').value;
        const novoTotal = document.getElementById('viewEditValorTotal').textContent.replace('R$ ', '').replace(',', '.');
        const novoEntregador = document.getElementById('viewEditEntregadorAtribuido').value;
        const novoPago = document.getElementById('viewEditPagoCheckbox').checked ? "Sim" : "Não";
        const novaTaxa = parseFloat(document.getElementById('viewEditTaxaEntrega').value).toFixed(2);

        const novasFormasPagamento = [];
        document.querySelectorAll('#viewEditForm input[name="viewEditFormaPagamento"]:checked').forEach(checkbox => {
            novasFormasPagamento.push(checkbox.value);
        });

        // Atualiza a linha da tabela
        selectedRow.dataset.status = novoStatus;
        selectedRow.dataset.total = novoTotal;
        selectedRow.dataset.entregador = novoEntregador;
        selectedRow.dataset.formasPagamento = novasFormasPagamento.join(',');
        selectedRow.dataset.pago = novoPago;
        selectedRow.dataset.taxa = novaTaxa;

        let badgeClass;
        switch (novoStatus) {
            case 'Aguardando Coleta':
                badgeClass = 'text-bg-secondary';
                break;
            case 'Em Trânsito':
                badgeClass = 'text-bg-warning';
                break;
            case 'Entregue':
                badgeClass = 'text-bg-success';
                break;
            case 'Cancelado':
                badgeClass = 'text-bg-danger';
                break;
        }
        selectedRow.cells[2].innerHTML = `<span class="badge badge-status rounded-pill ${badgeClass}">${novoStatus}</span>`;
        selectedRow.cells[3].textContent = novoEntregador;
        selectedRow.cells[4].textContent = `R$ ${parseFloat(novoTotal).toFixed(2).replace('.', ',')}`;

        viewEditModal.hide();
    }
});

// Lógica para impressão
function printOrder(row) {
    const data = row.dataset;
    const itens = JSON.parse(data.itens);
    const formasPagamento = data.formasPagamento ? data.formasPagamento.split(',') : [];

    let itensHtml = '';
    itens.forEach(item => {
        itensHtml += `
                    <tr>
                        <td>${item.quantidade}x</td>
                        <td>${item.nome}</td>
                        <td style="text-align: right;">R$ ${(item.quantidade * item.preco).toFixed(2).replace('.', ',')}</td>
                    </tr>
                `;
    });

    const printContent = `
                <div style="font-family: 'Poppins', sans-serif; padding: 20px; max-width: 600px; margin: auto; border: 1px solid #ddd; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                    <h2 style="text-align: center; color: #6c5ce7;">Recibo do Pedido</h2>
                    <hr style="border-top: 2px solid #6c5ce7;">
                    
                    <h4 style="color: #444;">Detalhes do Pedido</h4>
                    <p><strong>ID:</strong> ${data.id}</p>
                    <p><strong>Status:</strong> <span style="font-weight: bold; color: ${data.status === 'Entregue' ? '#28a745' : data.status === 'Em Trânsito' ? '#ffc107' : data.status === 'Aguardando Coleta' ? '#6c757d' : '#dc3545'};">${data.status}</span></p>
                    <p><strong>Entregador:</strong> ${data.entregador}</p>
                    <p><strong>Data/Hora:</strong> ${row.cells[5].textContent}</p>
                    
                    <h4 style="color: #444;">Dados do Cliente</h4>
                    <p><strong>Nome:</strong> ${data.cliente}</p>
                    <p><strong>Telefone:</strong> ${data.telefone}</p>
                    <p><strong>Endereço:</strong> ${data.endereco}</p>

                    <h4 style="color: #444;">Itens do Pedido</h4>
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;">
                        <thead>
                            <tr style="background-color: #f8f9fa;">
                                <th style="padding: 8px; border-bottom: 1px solid #ddd; text-align: left;">Qtd.</th>
                                <th style="padding: 8px; border-bottom: 1px solid #ddd; text-align: left;">Item</th>
                                <th style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">Preço</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${itensHtml}
                        </tbody>
                    </table>

                    <hr style="border-top: 1px dashed #bbb;">

                    <h4 style="color: #444;">Resumo do Pagamento</h4>
                    <p style="text-align: right;"><strong>Subtotal:</strong> R$ ${(data.total - data.taxa).toFixed(2).replace('.', ',')}</p>
                    <p style="text-align: right;"><strong>Taxa de Entrega:</strong> R$ ${parseFloat(data.taxa).toFixed(2).replace('.', ',')}</p>
                    <p style="text-align: right; font-size: 1.2em; font-weight: bold;">Valor Total: R$ ${parseFloat(data.total).toFixed(2).replace('.', ',')}</p>
                    
                    <p style="text-align: right;"><strong>Forma(s) de Pagamento:</strong> ${formasPagamento.join(', ')}</p>
                    <p style="text-align: right;"><strong>Status do Pagamento:</strong> ${data.pago === 'Sim' ? 'Já Pago' : 'Pendente'}</p>
                    
                    <p style="text-align: center; margin-top: 20px; font-style: italic; color: #888;">Obrigado pela preferência!</p>
                </div>
            `;

    const printWindow = window.open('', '_blank');
    printWindow.document.write(printContent);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
}