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
  admin_password                  = "Abcde12345-="
  disable_password_authentication = false
  network_interface_ids = [azurerm_network_interface.test.id]

  admin_ssh_key {
    username   = var.admin_username
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCt6bus8RoQdSu7gFtIjlT/oPaH9OFfG3oqpY2ztrNevoLF79GagNjn9nWbuXUYEZtl306gw/HM+pytesAMY/QJx7F1GFMvlJkoUyblHRkYeou0lYsQg7MSIrEMlc5ni9I6yxdV36RWUvDErpfCxmUat6yVflxNicqkrcfZB75mDslScrABH8Qc6UIHjNLx0lwtdDZ+rieEoaC4XFj7eMHVNoxn3HHRHVO03GM87rmg5g7PIh68bObGJqH6pK5Ft5GEaX+LGGKZulLBzpPmfq/C1AWttNdfyJteitxQCLMQ7HgVWV0aju51JaKe9WXHNIjBhw1EaiODgvSc9kKYUjvvlz+ahl1PFh5XbC00JWxzRr9iLj9fYxbL+mF5BgzGcrI/8KLIpkl/q8gzg31Jc7jVUnLcVYqmXqD0p2HS74uzJbtRv6IQr3kmSTd3qj/TCglZFFziFUR+xBo936guT5ZdwwO5uzUlUMogchFz1fZG03RS3jOqTpREY9t+NB5L9xE= thien@DESKTOP-HN8PQ6P"
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
