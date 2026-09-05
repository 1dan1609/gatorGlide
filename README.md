# GatorGlide Delivery Co. (GatorDelivery)

A custom order management and dispatch simulation backend built for GatorGlide Delivery Co.. Developed entirely in Python without external tree libraries, this system dynamically optimizes order fulfillment, calculates priority queues, and recalculates Estimated Times of Arrival (ETAs) in $O(\log n)$ time using synchronized AVL trees.

## System Architecture

The core routing and management engine relies on a dual-tree indexing system:
*   **Priority AVL Tree:** Indexes active orders by their calculated priority[cite: 2]. Duplicate priorities are handled by storing a set of order IDs at each node. This tree determines the exact queue order for the single delivery agent[cite: 2].
*   **ETA AVL Tree:** Indexes active orders strictly by their projected completion timestamp[cite: 2]. This allows the system to efficiently sweep and remove completed deliveries as the system time advances[cite: 2].

**Priority Calculation**  
Priority dynamically shifts based on the order's value and the time it was placed, using the following normalized equation[cite: 2]:  
$\text{priority} = 0.3 \times \left(\frac{\text{orderValue}}{50}\right) - 0.7 \times \text{currentSystemTime}$[cite: 2].

## Supported Operations

The system processes commands sequentially from an input file, supporting the following operations:
*   **`createOrder(orderId, currentSystemTime, orderValue, deliveryTime)`**: Computes the next available courier slot, assigns the ETA, prints which previously unfulfilled orders have been delivered, and shifts the ETAs of all lower-priority orders in the system[cite: 2].
*   **`cancelOrder(orderId, currentSystemTime)`**: Cancels pending orders (if not already out for delivery) and updates the ETAs of all remaining orders with a lower priority[cite: 2].
*   **`updateTime(orderId, currentSystemTime, newDeliveryTime)`**: Updates the transit duration required for an order and recalculates ETAs across all impacted lower-priority jobs[cite: 2].
*   **`print(orderId)`**: Outputs specific order details in the format `[orderId, currentSystemTime, orderValue, deliveryTime, ETA]`[cite: 2].
*   **`print(time1, time2)`**: Enumerates all undelivered orders scheduled to be completed within the specified time window[cite: 2].
*   **`getRankOfOrder(orderId)`**: Returns exactly how many orders will be delivered before the specified order ID[cite: 2].
*   **`Quit()`**: Terminates the program and prints the delivery details of all remaining orders[cite: 2].

## Usage and Execution

The program is designed to be executed via the command line, reading operations from a text file and outputting to an automatically generated results file[cite: 2].

**Run via Python:**
```bash
python3 gatorDelivery.py test.txt