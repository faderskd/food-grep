class RestaurantCreatedEvent {
  constructor(restaurant) {
    this.restaurant = restaurant;
  }
}

class RestaurantEditedEvent {
  constructor(restaurant, listIndex) {
    this.restaurant = restaurant;
    this.listIndex = listIndex;
  }
}

class RestaurantEditingEvent {
  constructor(restaurant, listIndex) {
    this.restaurant = restaurant;
    this.listIndex = listIndex;
  }
}


export {RestaurantCreatedEvent, RestaurantEditedEvent, RestaurantEditingEvent};