import { environment } from 'src/environments/environment';

export const API_URL = environment.apiUrl;
export const login_url = environment.login_url;

export default {
  PRODUCTS: API_URL + 'product/',
  SHOPS: API_URL + 'shop/',
  FAQ: API_URL + 'faq/',
  WISHLIST : API_URL + 'wishlist/'
};
