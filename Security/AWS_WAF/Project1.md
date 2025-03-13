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

