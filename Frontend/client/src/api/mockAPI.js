// Mock API - Replace with your actual API calls
export const mockAPI = {
  getRecommended: async (userId) => {
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      console.log(`Fetching recommendations for user ${userId}`);
      
      // Replace with: return axios.get(`http://127.0.0.1:8000/recommend/${userId}`)
      return {
        movies: [
          { 
            id: 1, 
            movie_id: 1,
            title: "The Shawshank Redemption", 
            poster_path: "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg", 
            overview: "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", 
            vote_average: 8.7, 
            release_date: "1994-09-23" 
          },
          { 
            id: 2, 
            movie_id: 2,
            title: "The Godfather", 
            poster_path: "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg", 
            overview: "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", 
            vote_average: 8.7, 
            release_date: "1972-03-14" 
          },
          { 
            id: 3, 
            movie_id: 3,
            title: "The Dark Knight", 
            poster_path: "/qJ2tW6WMUDux911r6m7haRef0WH.jpg", 
            overview: "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.", 
            vote_average: 8.5, 
            release_date: "2008-07-16" 
          },
          { 
            id: 4, 
            movie_id: 4,
            title: "Pulp Fiction", 
            poster_path: "/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg", 
            overview: "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.", 
            vote_average: 8.5, 
            release_date: "1994-09-10" 
          },
          { 
            id: 5, 
            movie_id: 5,
            title: "Forrest Gump", 
            poster_path: "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg", 
            overview: "The presidencies of Kennedy and Johnson unfold through the perspective of an Alabama man with an IQ of 75.", 
            vote_average: 8.4, 
            release_date: "1994-06-23" 
          },
        ]
      };
    } catch (error) {
      console.error('Error fetching recommended movies:', error);
      throw error;
    }
  },

  getSimilar: async (movieId) => {
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      console.log(`Fetching similar movies for movie ${movieId}`);
      
      // Replace with: return axios.get(`http://127.0.0.1:8000/recommend/similar/${movieId}`)
      return {
        movies: [
          { 
            id: 6, 
            movie_id: 6,
            title: "Inception", 
            poster_path: "/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg", 
            overview: "A thief who steals corporate secrets through dream-sharing technology.", 
            vote_average: 8.4, 
            release_date: "2010-07-15" 
          },
          { 
            id: 7, 
            movie_id: 7,
            title: "Interstellar", 
            poster_path: "/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg", 
            overview: "A team of explorers travel through a wormhole in space.", 
            vote_average: 8.3, 
            release_date: "2014-11-05" 
          },
          { 
            id: 8, 
            movie_id: 8,
            title: "The Matrix", 
            poster_path: "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg", 
            overview: "A computer hacker learns about the true nature of his reality.", 
            vote_average: 8.2, 
            release_date: "1999-03-30" 
          },
          { 
            id: 9, 
            movie_id: 9,
            title: "Gladiator", 
            poster_path: "/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg", 
            overview: "A former Roman General seeks vengeance against the corrupt emperor.", 
            vote_average: 8.1, 
            release_date: "2000-05-01" 
          },
          { 
            id: 10, 
            movie_id: 10,
            title: "The Prestige", 
            poster_path: "/tRNlZbgNCNOpLpbPEz5L8G8A0JN.jpg", 
            overview: "Two magicians engage in a competitive rivalry.", 
            vote_average: 8.0, 
            release_date: "2006-10-17" 
          },
        ]
      };
    } catch (error) {
      console.error('Error fetching similar movies:', error);
      throw error;
    }
  },

  getTrending: async () => {
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      console.log('Fetching trending movies');
      
      // Replace with: return axios.get(`http://127.0.0.1:8000/trending`)
      return {
        movies: [
          { 
            id: 11, 
            movie_id: 11,
            title: "Oppenheimer", 
            poster_path: "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", 
            overview: "The story of J. Robert Oppenheimer's role in developing the atomic bomb.", 
            vote_average: 8.3, 
            release_date: "2023-07-19" 
          },
          { 
            id: 12, 
            movie_id: 12,
            title: "Barbie", 
            poster_path: "/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg", 
            overview: "Barbie and Ken are having the time of their lives in Barbie Land.", 
            vote_average: 7.2, 
            release_date: "2023-07-19" 
          },
          { 
            id: 13, 
            movie_id: 13,
            title: "Dune: Part Two", 
            poster_path: "/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg", 
            overview: "Paul Atreides unites with Chani and the Fremen.", 
            vote_average: 8.4, 
            release_date: "2024-02-27" 
          },
        ]
      };
    } catch (error) {
      console.error('Error fetching trending movies:', error);
      throw error;
    }
  }
};