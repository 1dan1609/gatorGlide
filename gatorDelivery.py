import math
import sys

class order:
    def __init__(self,orderID, currentSystemTime, orderValue, deliveryTime, eta, priority):
        self.orderID=orderID
        self.currentSystemTime=currentSystemTime
        self.orderValue=orderValue
        self.deliveryTime=deliveryTime
        self.eta=eta
        self.priority=priority

class pTreeNode:
    def __init__(self, val, orderId):
        self.priority = val
        self.orders=set([orderId])
        self.left = None
        self.right = None
        self.height = 1

class Priority_Tree:
    def insert(self, root, priority, orderId):

        if not root: return pTreeNode(priority, orderId)
        elif priority < root.priority: root.left = self.insert(root.left, priority, orderId)
        elif priority == root.priority:
            root.orders.add(orderId)
        else: root.right = self.insert(root.right, priority, orderId)

        root.height = 1 + max(self.getHeight(root.left),
                           self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and priority < root.left.priority:
            return self.rightRotate(root)

        if balance < -1 and priority > root.right.priority:
            return self.leftRotate(root)

        if balance > 1 and priority > root.left.priority:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and priority < root.right.priority:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def delSmallest(self, root):
        if not root.left: return root.right
        else: root.left = self.delSmallest(root.left)

        root.height = 1 + max(self.getHeight(root.left),
                           self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and root.priority < root.left.priority:
            return self.rightRotate(root)

        if balance < -1 and root.priority > root.right.priority:
            return self.leftRotate(root)

        if balance > 1 and root.priority > root.left.priority:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and root.priority < root.right.priority:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def delete(self, root, orderId):
        target=orders_dict[orderId].priority
        if root.priority>target: root.left = self.delete(root.left, orderId)
        elif root.priority<target: root.right = self.delete(root.right, orderId)
        else:
            root.orders.remove(orderId)
            if len(root.orders)==0:
                if root.right:
                    nextNode=root.right
                    while nextNode.left: nextNode=nextNode.left
                    root.right=self.delSmallest(root.right)
                    root.priority=nextNode.priority
                    root.orders=nextNode.orders
                    del nextNode
                else:
                    root=root.left
        if not root: return None
        root.height = 1 + max(self.getHeight(root.left),
                          self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and root.priority < root.left.priority:
            return self.rightRotate(root)

        if balance < -1 and root.priority > root.right.priority:
            return self.leftRotate(root)

        if balance > 1 and root.priority > root.left.priority:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and root.priority < root.right.priority:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def searchMin(self, root, priority):
        prevBig=None
        temp=root
        while temp:
            if temp.priority==priority:
                prevBig=temp
                break
            elif temp.priority>priority:
                prevBig=temp
                temp=temp.left
            else:
                temp=temp.right
        return prevBig

    def update_ETAs(self, root, priority, updtime, inprocess=None):
        #UPDATES ETAS OF ALL LOWER PRIOIRITY ORDERS
        global myETAtree,ET
        updated=[]
        if priority>root.priority:
            if root.left: updated.extend(self.update_ETAs(root.left,priority, updtime, inprocess))
            for order in root.orders:
                if order==inprocess: continue
                myETAtree=ET.delete(myETAtree, order)
                newEta=orders_dict[order].eta+updtime
                myETAtree=ET.insert(myETAtree, newEta, order)
                orders_dict[order].eta=newEta
                updated.append(order)
            if root.right: updated.extend(self.update_ETAs(root.right,priority, updtime, inprocess))
        elif root.left: updated.extend(self.update_ETAs(root.left, priority, updtime, inprocess))
        return updated

    def leftRotate(self, x):
        y = x.right
        if not y: return x
        z = y.left if y else None

        y.left = x
        x.right = z

        x.height = 1 + max(self.getHeight(x.left),
                         self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(x.left),
                         self.getHeight(y.right))

        return y

    def rightRotate(self, x):
        y = x.left
        if not y: return x
        z = y.right if y else None

        y.right = x
        x.left = z

        x.height = 1 + max(self.getHeight(x.left),
                        self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(y.left),
                        self.getHeight(y.right))

        return y

    def getHeight(self, root):
        if not root: return 0
        return root.height

    def getBalance(self, root):
        if not root: return 0
        return self.getHeight(root.left) - self.getHeight(root.right)



class eTreeNode:
    def __init__(self, ETA, orderId):
        self.ETA = ETA
        self.orderId=orderId
        self.left = None
        self.right = None
        self.height = 1

class ETA_Tree:
    def insert(self, root, eta, orderId):

        if not root: return eTreeNode(eta,orderId)
        elif eta < root.ETA: root.left = self.insert(root.left, eta, orderId)
        else: root.right = self.insert(root.right, eta, orderId)


        root.height = 1 + max(self.getHeight(root.left),
                           self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and eta < root.left.ETA:
            return self.rightRotate(root)

        if balance < -1 and eta > root.right.ETA:
            return self.leftRotate(root)

        if balance > 1 and eta > root.left.ETA:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and eta < root.right.ETA:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def delSmallest(self, root):
        #Deletes smalles element in the given tree
        
        if not root.left: return root.right
        else: root.left = self.delSmallest(root.left)

        root.height = 1 + max(self.getHeight(root.left),
                           self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and root.ETA < root.left.ETA:
            return self.rightRotate(root)

        if balance < -1 and root.ETA > root.right.ETA:
            return self.leftRotate(root)

        if balance > 1 and root.ETA > root.left.ETA:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and root.ETA < root.right.ETA:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def delete(self, root, orderId):
        target=orders_dict[orderId].eta
        if root.ETA>target: root.left = self.delete(root.left, orderId)
        elif root.ETA<target: root.right = self.delete(root.right, orderId)
        else:
            if root.right:
                nextNode=root.right
                while nextNode.left: nextNode=nextNode.left
                root.right=self.delSmallest(root.right)
                root.ETA=nextNode.ETA
                root.orderId=nextNode.orderId
                del nextNode
            else:
                root=root.left

        if not root: return None
        root.height = 1 + max(self.getHeight(root.left),
                          self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and root.ETA < root.left.ETA:
            return self.rightRotate(root)

        if balance < -1 and root.ETA > root.right.ETA:
            return self.leftRotate(root)

        if balance > 1 and root.ETA > root.left.ETA:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and root.ETA < root.right.ETA:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def getRank(self, root, eta):
        if root==None: return 0
        if root.ETA<eta: return 1+self.getRank(root.left,eta)+self.getRank(root.right,eta)
        else: return self.getRank(root.left,eta)


    def searchMin(self, root, eta):
        #FINDS SMALLEST ETA JUST BIGGER THAN eta
        prevBig=None
        temp=root
        while temp:
            if temp.ETA>eta:
                prevBig=temp
                temp=temp.left
            else: temp=temp.right
        if prevBig: return prevBig.ETA, prevBig.orderId
        else: return math.inf, None

    def searchMax(self, root, eta):
        #FINDS LARGEST ETA JUST SMALLER THAN OR EQUAL TO eta
        prevSmall=None
        temp=root
        while temp:
            if temp.ETA==eta:
                prevSmall=temp
                break
            elif temp.ETA<eta:
                prevSmall=temp
                temp=temp.right
            else: temp=temp.left
        if prevSmall: return prevSmall.ETA, prevSmall.orderId
        else: return -math.inf, None

    def deliverTill(self, root, eta):
        #Completes and removes all deliveries till given time
        global myPriorityTree,PT,output
        if not root: return None
        if eta>=root.ETA:
            if root.left: root.left=self.deliverTill(root.left,eta)
            output.append(f"Order {root.orderId} has been delivered at time {root.ETA}")
            myPriorityTree=PT.delete(myPriorityTree,root.orderId)
            del orders_dict[root.orderId]
            if root.right: root.right=self.deliverTill(root.right,eta)
            return root.right

        #ELSE
        if root.left: root.left = self.deliverTill(root.left, eta)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and root.ETA < root.left.ETA:
            return self.rightRotate(root)

        if balance < -1 and root.ETA > root.right.ETA:
            return self.rightRotate(root)

        if balance > 1 and root.ETA > root.left.ETA:
            root.left=self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and root.ETA < root.right.ETA:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, x):
        y = x.right
        if not y: return x
        z = y.left if y else None

        y.left = x
        x.right = z

        x.height = 1 + max(self.getHeight(x.left),
                         self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(x.left),
                         self.getHeight(y.right))

        return y

    def rightRotate(self, x):
        y = x.left
        if not y: return x
        z = y.right if y else None

        y.right = x
        x.left = z

        x.height = 1 + max(self.getHeight(x.left),
                        self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(y.left),
                        self.getHeight(y.right))

        return y

    def getHeight(self, root):
        if not root: return 0
        return root.height

    def getBalance(self, root):
        if not root: return 0
        return self.getHeight(root.left) - self.getHeight(root.right)


myETAtree=None
myPriorityTree=None
ET=ETA_Tree()
PT=Priority_Tree()
orders_dict={}
output=[]

def Print(par1, par2=None):
    global myETAtree, ET, output
    if not par2: #Alternative to the lack of support of function overloading
        # for 'print(orderId)'
        orderId=par1
        if orderId in orders_dict:
            CurOrder = orders_dict[orderId]
            output.append(f"[{CurOrder.orderID},{CurOrder.currentSystemTime},{CurOrder.orderValue},{CurOrder.deliveryTime},{CurOrder.eta}]")
        else: output.append(f"No order with order Id {orderId}")
    else:
        #for 'print(tim1, time2)'
        time1,time2=par1,par2
        order_list=[]
        while time1<time2:
            time1,orderID=ET.searchMin(myETAtree, time1)
            if time1>time2: break
            order_list.append(orderID)
        if not order_list: output.append("There are no orders in that time period")
        else: output.append(str(order_list))
    
    for i in output: print(i)
    output=[]

def getRankOfOrder(orderId):
    global myETAtree, ET, output
    if orderId not in orders_dict: return
    eta=orders_dict[orderId].eta
    rank=ET.getRank(myETAtree, eta)
    output.append(f"Order {orderId} will be delivered after {rank} orders")
    for op in output:
        print(op)
    output=[]

def createOrder(order_id, currentSystemTime, orderValue, deliveryTime):
    global myETAtree, myPriorityTree, ET, PT, output
    prevEta, prevOrder = ET.searchMax(myETAtree, currentSystemTime)
    nextEta, nextOrder = ET.searchMin(myETAtree, currentSystemTime)
    inprocess=None
    
    if prevOrder and prevEta+orders_dict[prevOrder].deliveryTime>currentSystemTime:
        #Delivery person is not free and returning from a previous order
        next_avlb_time=prevEta+orders_dict[prevOrder].deliveryTime
    elif nextOrder and nextEta-orders_dict[nextOrder].deliveryTime<currentSystemTime:
        #Delivery person dispatched for next delivery
        next_avlb_time=nextEta+orders_dict[nextOrder].deliveryTime
        inprocess=nextOrder
    else: next_avlb_time=currentSystemTime

    priority=0.3*(orderValue/50)-0.7*currentSystemTime
    myETAtree=ET.deliverTill(myETAtree, currentSystemTime)
    previous=PT.searchMin(myPriorityTree, priority)

    if not previous:
        new_eta=next_avlb_time+deliveryTime
    else:
        max_eta=0
        for prev_order in previous.orders:
            if max_eta<orders_dict[prev_order].eta:
                max_eta=orders_dict[prev_order].eta
                prev_max_order=prev_order
        new_eta=max_eta+orders_dict[prev_max_order].deliveryTime+deliveryTime
    
    orders_dict[order_id]=order(order_id, currentSystemTime, orderValue, deliveryTime, new_eta, priority)
    myPriorityTree=PT.insert(myPriorityTree, priority, order_id)
    myETAtree=ET.insert(myETAtree,new_eta,order_id)

    output=[f"Order {order_id} has been created - ETA: {new_eta}"]+output
    updated=PT.update_ETAs(myPriorityTree, priority, deliveryTime*2, inprocess)
    if updated:
        updated.sort(key=lambda x: orders_dict[x].eta)
        output.append("Updated ETAs: [")
        for i in range(len(updated)):
            #Condition to differentiate between , and ]
            if i == len(updated)-1: output[-1]+=f"{updated[i]}:{orders_dict[updated[i]].eta}]"
            else: output[-1]+=f"{updated[i]}:{orders_dict[updated[i]].eta}, "
    for op in output: print(op)
    output=[]


def cancelOrder(order_id, currentSystemTime):
    global myETAtree, myPriorityTree, ET, PT, output
    if order_id not in orders_dict or orders_dict[order_id].eta<currentSystemTime: output.append(f"Cannot cancel. Order {order_id} has already been delivered.")
    elif orders_dict[order_id].eta - orders_dict[order_id].deliveryTime < currentSystemTime: output.append(f"Cannot cancel. Order {order_id} is already out for delivery")
    else:
        myETAtree=ET.delete(myETAtree, order_id)
        myPriorityTree=PT.delete(myPriorityTree, order_id)
        updated=PT.update_ETAs(myPriorityTree, orders_dict[order_id].priority, -orders_dict[order_id].deliveryTime*2)
        output.append(f"Order {order_id} has been canceled.")
        if updated:
            updated.sort(key=lambda x: orders_dict[x].eta)
            output.append("Updated ETAs: [")
            for i in range(len(updated)):
                #Condition to differentiate between , and ]
                if i == len(updated)-1: output[-1]+=f"{updated[i]}:{orders_dict[updated[i]].eta}]"
                else: output[-1]+=f"{updated[i]}:{orders_dict[updated[i]].eta}, "
        del orders_dict[order_id]
    myETAtree=ET.deliverTill(myETAtree, currentSystemTime)
    for op in output: print(op)
    output=[]

def updateTime(order_id, currentSystemTime, newDeliveryTime):
    global myETAtree, myPriorityTree, ET, PT, output
    if orders_dict[order_id].eta<currentSystemTime: output.append(f"Cannot update. Order {order_id} has already been delivered.")
    elif orders_dict[order_id].eta - orders_dict[order_id].deliveryTime <currentSystemTime: output.append(f"Cannot update. Order {order_id} is already out for delivery")
    else:
        myETAtree=ET.delete(myETAtree, order_id)
        newETA=orders_dict[order_id].eta - orders_dict[order_id].deliveryTime + newDeliveryTime
        myETAtree=ET.insert(myETAtree, newETA,order_id)
        orders_dict[order_id].eta=newETA

        updtime=(newDeliveryTime*2) - (orders_dict[order_id].deliveryTime*2)
        orders_dict[order_id].deliveryTime=newDeliveryTime
        updated=[order_id]
        updated.extend(PT.update_ETAs(myPriorityTree, orders_dict[order_id].priority,updtime))
        updated.sort(key=lambda x: orders_dict[x].eta)
        output.append("Updated ETAs: [")
        for i in range(len(updated)):
            #Condition to differentiate between , and ]
            if i == len(updated)-1: output[-1]+=f"{updated[i]}:{orders_dict[updated[i]].eta}]"
            else: output[-1]+=f"{updated[i]}:{orders_dict[updated[i]].eta}, "
    
    myETAtree=ET.deliverTill(myETAtree, currentSystemTime)
    for op in output: print(op)
    output=[]

def Quit():
    global myETAtree,ET, output
    myETAtree=ET.deliverTill(myETAtree, math.inf)
    for op in output: print(op)
    output=[]


ipname=sys.argv[1]
if len(ipname)>4 and ipname[-4:]=='.txt': ipname=ipname[:-4]
with open(ipname+'.txt') as f_in:
    commands = []
    for l in f_in:
        l = l.strip('\n')
        if l and l[0]=='p': l='P'+l[1:]
        commands.append(l)
        
opfil=open(ipname+'_output_file.txt', "a")
ogout=sys.stdout
sys.stdout = opfil
for l in commands:
    if eval(l)!=None:
        eval(l)
sys.stdout=ogout
opfil.close()
f_in.close()