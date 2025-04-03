import React from 'react';

export default function PrivacyPolicyPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8">Privacy Policy</h1>
        
        <div className="prose prose-lg max-w-none">
          <p className="text-gray-500 mb-8 text-center">Last Updated: June 15, 2023</p>
          
          <h2 className="text-2xl font-semibold mb-4">1. Introduction</h2>
          <p className="mb-6">
            At Afri Furn, we respect your privacy and are committed to protecting your personal data. This privacy policy will inform you about how we look after your personal data when you visit our website and tell you about your privacy rights and how the law protects you.
          </p>
          
          <h2 className="text-2xl font-semibold mb-4">2. The Data We Collect About You</h2>
          <p className="mb-4">
            Personal data, or personal information, means any information about an individual from which that person can be identified. We may collect, use, store and transfer different kinds of personal data about you which we have grouped together as follows:
          </p>
          <ul className="list-disc pl-6 mb-6">
            <li className="mb-2"><strong>Identity Data</strong> includes first name, last name, username or similar identifier.</li>
            <li className="mb-2"><strong>Contact Data</strong> includes billing address, delivery address, email address and telephone numbers.</li>
            <li className="mb-2"><strong>Financial Data</strong> includes payment card details.</li>
            <li className="mb-2"><strong>Transaction Data</strong> includes details about payments to and from you and other details of products you have purchased from us.</li>
            <li className="mb-2"><strong>Technical Data</strong> includes internet protocol (IP) address, your login data, browser type and version, time zone setting and location, browser plug-in types and versions, operating system and platform, and other technology on the devices you use to access this website.</li>
            <li className="mb-2"><strong>Profile Data</strong> includes your username and password, purchases or orders made by you, your preferences, feedback and survey responses.</li>
            <li className="mb-2"><strong>Usage Data</strong> includes information about how you use our website and products.</li>
            <li><strong>Marketing and Communications Data</strong> includes your preferences in receiving marketing from us and our third parties and your communication preferences.</li>
          </ul>
          
          <h2 className="text-2xl font-semibold mb-4">3. How We Use Your Personal Data</h2>
          <p className="mb-4">
            We will only use your personal data when the law allows us to. Most commonly, we will use your personal data in the following circumstances:
          </p>
          <ul className="list-disc pl-6 mb-6">
            <li className="mb-2">Where we need to perform the contract we are about to enter into or have entered into with you.</li>
            <li className="mb-2">Where it is necessary for our legitimate interests (or those of a third party) and your interests and fundamental rights do not override those interests.</li>
            <li>Where we need to comply with a legal obligation.</li>
          </ul>
          
          <h2 className="text-2xl font-semibold mb-4">4. Data Security</h2>
          <p className="mb-6">
            We have put in place appropriate security measures to prevent your personal data from being accidentally lost, used or accessed in an unauthorized way, altered or disclosed. In addition, we limit access to your personal data to those employees, agents, contractors and other third parties who have a business need to know. They will only process your personal data on our instructions and they are subject to a duty of confidentiality.
          </p>
          
          <h2 className="text-2xl font-semibold mb-4">5. Data Retention</h2>
          <p className="mb-6">
            We will only retain your personal data for as long as reasonably necessary to fulfill the purposes we collected it for, including for the purposes of satisfying any legal, regulatory, tax, accounting or reporting requirements. We may retain your personal data for a longer period in the event of a complaint or if we reasonably believe there is a prospect of litigation in respect to our relationship with you.
          </p>
          
          <h2 className="text-2xl font-semibold mb-4">6. Your Legal Rights</h2>
          <p className="mb-4">
            Under certain circumstances, you have rights under data protection laws in relation to your personal data, including the right to:
          </p>
          <ul className="list-disc pl-6 mb-6">
            <li className="mb-2">Request access to your personal data.</li>
            <li className="mb-2">Request correction of your personal data.</li>
            <li className="mb-2">Request erasure of your personal data.</li>
            <li className="mb-2">Object to processing of your personal data.</li>
            <li className="mb-2">Request restriction of processing your personal data.</li>
            <li className="mb-2">Request transfer of your personal data.</li>
            <li>Right to withdraw consent.</li>
          </ul>
          
          <h2 className="text-2xl font-semibold mb-4">7. Cookies</h2>
          <p className="mb-6">
            You can set your browser to refuse all or some browser cookies, or to alert you when websites set or access cookies. If you disable or refuse cookies, please note that some parts of this website may become inaccessible or not function properly.
          </p>
          
          <h2 className="text-2xl font-semibold mb-4">8. Changes to the Privacy Policy</h2>
          <p className="mb-6">
            We may update our privacy policy from time to time. We will notify you of any changes by posting the new privacy policy on this page and updating the "Last Updated" date at the top of this privacy policy.
          </p>
          
          <h2 className="text-2xl font-semibold mb-4">9. Contact Us</h2>
          <p className="mb-6">
            If you have any questions about this privacy policy or our privacy practices, please contact us at:
          </p>
          <div className="bg-gray-100 p-6 rounded-lg mb-6">
            <p className="mb-1"><strong>Email:</strong> privacy@afrifurn.com</p>
            <p className="mb-1"><strong>Phone:</strong> +254 700 123 456</p>
            <p><strong>Address:</strong> 123 Furniture Lane, Nairobi, Kenya</p>
          </div>
        </div>
      </div>
    </div>
  );
} 