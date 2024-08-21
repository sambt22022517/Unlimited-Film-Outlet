import PurchaseHistory from '../components/PurchaseHistory';

const PurchaseHistoryPage = () => {
  const purchaseData = [
    {
      date: '2024-08-16',
      movies: [
        { title: 'Presumed Innocent', price: 14.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/p-dFQhrrenz0eg8_smgu9w/369x208.jpg' },
        { title: 'Lady in the Lake', price: 19.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/SCG2BRdS-gXePqsduWlMmQ/369x208.jpg' },
      ],
      totalPrice: 34.98
    },
    {
      date: '2024-08-10',
      movies: [
        { title: 'Ted Lasso', price: 9.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/ageP1PYyLi7UlNiWMva32Q/369x208.jpg' },
      ],
      totalPrice: 9.99
    },
    {
      date: '2024-08-07',
      movies: [
        { title: 'Presumed Innocent', price: 14.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/p-dFQhrrenz0eg8_smgu9w/369x208.jpg' },
        { title: 'Lady in the Lake', price: 19.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/SCG2BRdS-gXePqsduWlMmQ/369x208.jpg' },
        { title: 'Presumed Innocent', price: 14.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/p-dFQhrrenz0eg8_smgu9w/369x208.jpg' },
        { title: 'Lady in the Lake', price: 19.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/SCG2BRdS-gXePqsduWlMmQ/369x208.jpg' },
        { title: 'Presumed Innocent', price: 14.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/p-dFQhrrenz0eg8_smgu9w/369x208.jpg' },
        { title: 'Lady in the Lake', price: 19.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/SCG2BRdS-gXePqsduWlMmQ/369x208.jpg' },
      ],
      totalPrice: 104.94
    },
  ];

  return (
    <div className="PurchaseHistoryPage">
      <PurchaseHistory purchases={purchaseData} />
    </div>
  );
};

export default PurchaseHistoryPage;
