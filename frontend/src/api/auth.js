import api from '../api'



export const register = (data) => {
    return api.post('api/register/', data);
}

export const verifyEmail = (userId, code) => {
    return api.post(`api/verify-email/${userId}/`, code);
}

export const resendCode = (userId) => {
    return api.post(`api/resend-email/${userId}/`);
}


export const login = (credentials) => {
    return api.post('api/login/', credentials);
}

export const logout = () => {
    return api.post('api/logout/');
}