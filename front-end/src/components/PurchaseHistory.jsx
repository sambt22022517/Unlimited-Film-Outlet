import PurchaseHistoryItem from './PurchaseHistoryItem';
import '../styles/PurchaseHistory.css';

const PurchaseHistory = ({ purchases }) => {
  return (
    <div className="purchase-history">
      <h1>Purchase History</h1>
      <div className="purchase-history-list">
        {purchases.map((purchase, index) => (
          <PurchaseHistoryItem key={index} item={purchase} />
        ))}
      </div>
    </div>
  );
};

export default PurchaseHistory;