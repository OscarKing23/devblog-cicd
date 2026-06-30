from datetime import datetime
from typing import Dict, List, Optional


class BlogPost:
    def __init__(self, title: str, content: str, author: str = "Admin"):
        """Constructor del post."""
        self.id = None
        self.title = title.strip()
        self.content = content.strip()
        self.author = author.strip()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @property
    def summary(self) -> str:
        """Resumen para la lista de posts."""
        return self.content[:150] + "..." if len(self.content) > 150 else self.content

    def to_dict(self) -> Dict:
        """Convierte el post a diccionario para JSON/API."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": self.summary,
        }

    def update(self, title: str = None, content: str = None):
        """Actualiza el post con nuevos datos."""
        if title:
            self.title = title.strip()
        if content:
            self.content = content.strip()
        self.updated_at = datetime.now()


class BlogStorage:
    """Almacenamiento en memoria para los posts del blog."""

    def __init__(self):
        self._posts: List[BlogPost] = []
        self._next_id = 1
        self._create_sample_posts()

    def _create_sample_posts(self):
        """Crea posts de ejemplo para demostracion."""
        sample_posts = [
            {
                "title": "Bienvenido a DevBlog!",
                "content": """Este es mi primer post en DevBlog, una
aplicacion creada para aprender DevOps y CI/CD.

En este blog compartire mi experiencia aprendiendo:
- Desarrollo web con Flask
- Containerizacion con Docker
- Testing automatizado
- CI/CD con GitHub Actions
- Despliegue en la nube

Espero que disfrutes leyendo tanto como yo disfruto escribiendo!""",
                "author": "DevOps Student",
            },
            {
                "title": "Mi experiencia con Docker",
                "content": """Docker ha sido una revelacion en mi aprendizaje de DevOps.
La capacidad de empaquetar una aplicacion con todas sus dependencias en un contenedor portable es increible.
Ya no mas "en mi maquina funciona".

Algunos beneficios que he descubierto:
- Consistencia entre entornos
- Facil escalabilidad
- Aislamiento de aplicaciones
- Despliegues mas confiables

Cual ha sido tu experiencia con Docker?""",
                "author": "DevOps Student",
            },
        ]

        for post_data in sample_posts:
            post = BlogPost(
                title=post_data["title"],
                content=post_data["content"],
                author=post_data["author"],
            )
            self.create_post(post)

    def create_post(self, post: BlogPost) -> BlogPost:
        """Crea un nuevo post."""
        post.id = self._next_id
        self._next_id += 1
        self._posts.append(post)
        return post

    def get_all_posts(self) -> List[BlogPost]:
        """Obtiene todos los posts ordenados por fecha."""
        return sorted(self._posts, key=lambda x: x.created_at, reverse=True)

    def get_post_by_id(self, post_id: int) -> Optional[BlogPost]:
        """Busca un post por su ID."""
        for post in self._posts:
            if post.id == post_id:
                return post
        return None

    def update_post(
        self, post_id: int, title: str = None, content: str = None
    ) -> Optional[BlogPost]:
        """Actualiza un post existente."""
        post = self.get_post_by_id(post_id)
        if post:
            post.update(title, content)
            return post
        return None

    def delete_post(self, post_id: int) -> bool:
        """Elimina un post."""
        post = self.get_post_by_id(post_id)
        if post:
            self._posts.remove(post)
            return True
        return False

    def search_posts(self, query: str) -> List[BlogPost]:
        """Busca posts por titulo o contenido."""
        query = query.lower().strip()
        if not query:
            return self.get_all_posts()

        results = []
        for post in self._posts:
            if query in post.title.lower() or query in post.content.lower():
                results.append(post)

        results.sort(
            key=lambda x: (
                query not in x.title.lower(),
                -x.created_at.timestamp(),
            )
        )
        return results


blog_storage = BlogStorage()
