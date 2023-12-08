resource "azurerm_network_interface" "test" {
  name                = "NIC-${var.resource_type}-${var.application_type}"
  location            = var.location
  resource_group_name = var.resource_group

  ip_configuration {
    name                          = "internal"
    subnet_id                     = var.public_subnet_id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = var.public_ip_address_id
  }
}

resource "azurerm_linux_virtual_machine" "test" {
 name                  = "${var.resource_type}-${var.application_type}"
  location              = var.location
  resource_group_name   = var.resource_group
  size                  = "Standard_B1s"
  admin_username        = var.admin_username
  disable_password_authentication = false
  network_interface_ids = [azurerm_network_interface.test.id]

  admin_ssh_key {
    username   = var.admin_username
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDlLF8M7VHy5U6YVkNBq8Xypf0iNu2pi7B//soY7ZLJ1muqQOuG7Ds15UZK8e3YQnbQGq0Nkt3bPMjxzAfXLvD0xHp0e0xzrBLTrkvrS9mx9IO4jevr0OA1dNTlHAc9nX1a4S+jm7QtgZ3DlwoxdE0phKXSDtmLjIfFTvCNRmnQ3d8cVolUVgSyvTACaXI1r14dPvZeyPmUXV68hxOT4SPeQdWfjhvdtqVQ/hdLu2oyUUqDctruTkilCPdafT4nXCzNy66Nm8q4Dy4jbUf5b20q9N582NfpV1VQbWCz1R/7wPIfObC0l6gWdXccgt/wepOjH5V346lT87+GYBOkkqbLpFHwls0NsFdF6+SPfjCd1qkfClsKaXKwq0IIUGOwKRy2LRFXqNWxSNAD1EOzSLkNQoEa2HpkpEKzIGOV4E9HJJ/7xAJbJdrcNn9uEcobJ1qu7OZ8Uaq+IekpjzfuST8KAtg5qfaILEYOmm6GueLDbrr+8R74WXY5uHUXj+XJ1jc= phongmx\phongmx@PhongMX"
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}
