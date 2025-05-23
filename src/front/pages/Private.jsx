import React, { useEffect, useState } from "react";
import useGlobalReducer from "../hooks/useGlobalReducer";
import { useNavigate } from "react-router-dom";
import { getUsers } from "../store";

const Private = () => {
    const { store, dispatch } = useGlobalReducer();
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("token");
        console.log("Token en Private.jsx antes de getUsers:", token);

        if (!token) {
            navigate('/login');
            return;
        }

        getUsers(dispatch);
    }, [dispatch, navigate]);

    const users = Array.isArray(store.users) ? [...store.users].reverse() : [];

    return (
        <div className="container my-4">
            <ul className="list-group">
                {users.length === 0 ? (
                    <li className="list-group-item">Cargando usuarios...</li>
                ) : (
                    users.map((user, index) => (
                        <li key={index} className="list-group-item d-flex justify-content-between align-items-start">
                            <div className="ms-2 me-auto">
                                <div className="fw-bold">User ID: {user.id}</div>
                                {user.email}
                            </div>
                            <span className={`badge ${user.is_active ? 'bg-success' : 'bg-danger'} rounded-pill`}>
                                {user.is_active ? 'Active' : 'Inactive'}
                            </span>
                        </li>
                    ))
                )}
            </ul>
        </div>
    );
};

export default Private;
