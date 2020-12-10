# [MMC Web Inventory Tracker](http://mmcinventory.herokuapp.com)

## A web-based inventory tracking app for the machining department at [Millerbernd Manufacturing Company](http://www.millerberndmfg.com/ring-cylinder/products/cnc-machining/).

### Purpose
---
This web-app is designed to keep track of tooling materials for the machining department. It records which storage locations a given item can be found in, as well as the number of items in that location.

Each time an employee checks out an item and doesn't replace it, the app records details about the discrepancy, including the time, the amount, and the employee who caused it. Management can make freeform modifications to item details and quantities, which are also recorded in detail.

### Usage
---
#### Navigation

##### Browse Inventory

In addition to using the search bar at the top of the page, you can browse the entire inventory by selecting "Browse Inventory" from the sidebar of any page. Here you have the option to browse items filtered by Category, Storage Location, Manufacturer, or simply viewing all items. Once you locate the item you are looking for, you can view its full details including a part number, complete description, storage locations, and the quantity of that item currently checked out to other employees.

##### Current Picklists

Here you can see a list of existing picklists created by any employee. Open picklists can be modified and checked out, and checked out picklists can be checked back in. More details on picklist usage can be found under [Using Picklists](#Using-picklists).

##### Adjustment History

This page is only accessible to employees with a valid manager login. Here you will find a complete history of changes made to the inventory. Similar to the [Browse Inventory](#Browse-Inventory) page, you can browse by a variety of filters including employee who made the change, the reason for the change, the date the change occurred, and the item that was changed. Note that picklists do not appear here unless the number of items checked in was different than the amount checked out.

##### Management

This page is only accessible to employees with a valid manager login. This page allows you to make freeform changes to the inventory. You can create new items, directly modify an items storage locations and quantities, and modify and items details, such as part number and description. Note that more advanced tasks like item deletion, category creation, and bulk modifications will require direct access to the sites database.

#### Using Picklists

Picklists are a simple way for employees to keep track of things they have taken and returned to their storage locations, without worrying about accidentally making unwanted changes to the inventory. Anyone can see picklists created by any employee, so employees can continue working on picklists created by other shifts, supervisors, or programmers.

To begin, simply enter a title for your picklist and click the "Create Picklist" button on the right sidebar. This title can be anything, but make it descriptive such as the name of the machine you are running, or the customer part number you are working on. If someone else already started a picklist for you, you can find it on the [Current Picklists](#Current-picklists) page under "Open".

To add and item to a picklist, simply [browse to the items detail page](#browse-inventory) and under "Locations" click "Add to List" next to the storage location you will be taking the item from. To remove an item from a picklist, hover over the item on the right sidebar and click the trash can icon that appears. When you are finished adding items, you can save the picklist for someone else to use later by clicking the "Save" button at the bottom of the picklist sidebar.

Once you have located all the items on your picklist and are ready to checkout, simply click the "Checkout" button at the bottom of the picklist sidebar. This will move the picklist to the "Checked Out" section on the [Current Picklists](#current-picklists) page. When you are finished using the tools you can click the "Check In" button next to your picklist on that page.

When checking in a picklist, be sure to enter how many of each item you are returning. For consumable items such as carbide inserts, simply enter 0 and the site will record that item as used so more can be ordered to replace it. If you make an error when checking in a picklists, notify someone with management login credentials and they can correct the error.

### Restrictions
---
The site can be browsed freely using the demo credentials below,however, modifying picklists or items requires a valid employee login. Freeform modification of inventory quantities required an approved management login.

DEMO ID: 1111  
DEMO Password: 1111
