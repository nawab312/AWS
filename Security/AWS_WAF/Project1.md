## ALB integrate with AWS WAF ##

- **Attaching AWS WAF to ALB**
  - AWS WAF operates at *Layer 7 (Application Layer)* and can be directly associated with an ALB.
  - You create a *WebACL (Web Access Control List)* in AWS WAF and associate it with your ALB.
  - The WebACL consists of rules that allow, block, or count requests based on various conditions.
 
- **How AWS WAF Works with ALB**
  - When a request reaches ALB, AWS WAF evaluates the request *before forwarding it to the target group*
  - If the request matches a *deny rule*, AWS WAF blocks it, and ALB never forwards it to the backend.
  - If the request is *allowed*, ALB routes it to the appropriate target based on routing rules.

- I already have three EC2 instances behind an ALB:
  
![image](https://github.com/user-attachments/assets/d243218c-bf8c-402e-93cc-dfa19a0caf16)

- I simple create a Web ACL in the same region and associate it with the ALB. I begin by naming the Web ACL. I also instruct WAF to publish to a designated CloudWatch metric:

![image](https://github.com/user-attachments/assets/4b793477-4454-48ce-a1a4-d55c0b49f634)

- Add Conditions (Rules): You can add multiple conditions (rules) based on your security needs:
  - **Add Managed Rules (Pre-configured by AWS)**
    - Click Add Rules → Choose Add managed rule groups.
    - Select AWS Managed Rule Groups, such as:
       - `AWS-AWSManagedRulesSQLiRuleSet` → Blocks SQL Injection.
       - `AWS-AWSManagedRulesCommonRuleSet` → Protects against common attacks.
       - `AWS-AWSManagedRulesBotControlRuleSet` → Blocks bots.
  
  ![image](https://github.com/user-attachments/assets/094804a6-1f05-4544-bb6c-ac6671dfe7e4)

  - **Add Custom Rules**
    - To create your own conditions, select Add my own rules and rule groups → Click Add Rule.
    - *Block Requests from Specific IPs*
      - Select Rule Type → Choose IP Set.
      - Create an IP Set (e.g., `BlockedIPs`) and enter IP addresses to block.
      - Choose Action → Block.

  ![image](https://github.com/user-attachments/assets/738ac885-4ef7-4b76-9aaf-00fd81fd3a3d)

