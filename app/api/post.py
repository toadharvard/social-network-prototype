from fastapi import APIRouter, Body, Depends, Path

from app.deps import *
from app.dto.post import *
from app.usecase import UseCase

router = APIRouter(prefix="/post", tags=["Posts (articles)"])


@router.post("", response_model=PostResponse)
def create_post(
    use_case: UseCase = Depends(),
    user=Depends(get_current_user),
    payload: CreatePostRequest = Body(),
):
    payload = CreatePostSchema(**payload.dict(), owner_id=user.id)
    return use_case.post.create(obj_in=payload)


@router.get(
    "/all",
    response_model=list[PostResponse],
    dependencies=[Depends(get_current_user)],
)
def get_all_posts(
    req: PageRequest = Depends(),
    use_case: UseCase = Depends(),
):
    items = map(
        use_case.post.enrich_with_reactions,
        use_case.post.get_all(req.skip, req.limit),
    )
    return list(items)


@router.patch(
    "/{post_id}",
    response_model=PostResponse,
    dependencies=[Depends(get_user(is_post_owner=True))],
)
def update_post(
    use_case: UseCase = Depends(),
    post=Depends(get_current_post),
    payload: UpdatePostSchema = Body(),
):
    return use_case.post.enrich_with_reactions(
        use_case.post.update(db_obj=post, obj_in=payload)
    )


@router.delete(
    "/{post_id}",
    response_model=PostResponse,
)
def delete_post(
    post=Depends(get_current_post),
    use_case: UseCase = Depends(),
    user=Depends(get_user(is_post_owner=True)),
):
    use_case.post.remove_all_reactions(post, user)
    return use_case.post.remove(id=post.id)


@router.post("/{post_id}/reaction/{reaction}", tags=["Reactions"])
def add_reaction(
    reaction: PostReaction = Path(),
    use_case: UseCase = Depends(),
    user=Depends(get_user(is_post_owner=False)),
    post=Depends(get_current_post),
):
    use_case.post.add_reaction(post, user, reaction)
    return f"Reaction {reaction} added"


@router.delete("/{post_id}/reaction/{reaction}", tags=["Reactions"])
def remove_reaction(
    reaction: PostReaction = Path(),
    use_case: UseCase = Depends(),
    user=Depends(get_user(is_post_owner=False)),
    post=Depends(get_current_post),
):
    use_case.post.remove_reaction(post, user, reaction)
    return f"Reaction {reaction} removed"


@router.delete("/{post_id}/reaction/all", tags=["Reactions"])
def remove_all_reactions(
    use_case: UseCase = Depends(),
    user=Depends(get_user(is_post_owner=False)),
    post=Depends(get_current_post),
):
    use_case.post.remove_all_reactions(post, user)
    return f"All reactions are removed"
