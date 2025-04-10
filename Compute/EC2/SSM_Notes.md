Amazon SSM (AWS Systems Manager) is a service that lets you manage, automate, and securely access your EC2 and on-premises servers without needing SSH or bastion hosts. It provides features like remote command execution, patching, configuration management, and secure session access using IAM controls.

SSM uses a secure, *outbound HTTPS connection* initiated by the SSM Agent on the instance. This is fundamentally different from SSH or traditional client-server models.

**Core Networking Model: Pull Architecture**

![image](https://github.com/user-attachments/assets/ad1de46c-a1a9-409f-b267-9de9b0f4d61f)
