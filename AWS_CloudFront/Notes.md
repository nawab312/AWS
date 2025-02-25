Amazon CloudFront is a **content delivery network (CDN)** service provided by AWS that securely delivers data, videos, applications, and APIs to users with **low latency** and **high transfer speeds**. It uses a network of globally distributed **edge locations** to cache and serve content closer to end users.
- CloudFront has over **450 Points of Presence (PoPs)** across the globe, ensuring that content is served from a location nearest to the user.
- By caching static and dynamic content at edge locations, CloudFront reduces round-trip times and accelerates content delivery.
- Static Content (Images, Videos, CSS, JavaScript, etc.) is cached at edge locations.
- Dynamic Content (API responses, HTML pages) is delivered with **Lambda@Edge** or **Origin Shield**.
