import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

export const Navbar = () => {
	const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));
	const navigate = useNavigate();

	const handleLogout = () => {
		localStorage.removeItem("token");
		setIsLoggedIn(false);
		navigate("/");
	};

	useEffect(() => {

		const handleStorageChange = () => {
			setIsLoggedIn(!!localStorage.getItem("token"));
		};


		const interval = setInterval(() => {
			setIsLoggedIn(!!localStorage.getItem("token"));
		}, 1000);

		window.addEventListener("storage", handleStorageChange);

		return () => {
			window.removeEventListener("storage", handleStorageChange);
			clearInterval(interval);
		};
	}, []);

	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/" className="navbar-brand mb-0 h1">
					React Boilerplate
				</Link>

				<div className="d-flex">
					<Link to="/demo">
						<button className="btn btn-primary me-2">Check the Context</button>
					</Link>

					{!isLoggedIn ? (
						<>
							<Link to="/signup">
								<button type="button" className="btn btn-dark me-2">Signup</button>
							</Link>
							<Link to="/login">
								<button type="button" className="btn btn-dark">Login</button>
							</Link>
						</>
					) : (
						<button onClick={handleLogout} className="btn btn-danger">Logout</button>
					)}
				</div>
			</div>
		</nav>
	);
};
