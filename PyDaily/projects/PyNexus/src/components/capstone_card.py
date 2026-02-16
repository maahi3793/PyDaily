"""
Capstone Card Component - Individual story card for the Capstone board.
"""
import flet as ft


def build_capstone_card(story: dict, status: str, on_start, on_test, on_continue, retries: int = 0):
    """
    Build a story card for the Capstone board.
    
    Args:
        story: Story data from DB
        status: 'backlog', 'ready', 'in_progress', 'shipped'
        on_start: Callback for START button
        on_test: Callback for TEST button
        on_continue: Callback for CONTINUE/folder button
        retries: Number of failed test attempts
    """
    story_code = story.get('story_code', '')
    title = story.get('title', 'Untitled')
    description = story.get('description', '')
    xp = story.get('xp', 10)
    
    # Color based on status and retries
    if status == 'shipped':
        border_color = ft.Colors.GREEN_400
    elif retries >= 3:
        border_color = ft.Colors.RED_400
    elif retries >= 1:
        border_color = ft.Colors.PURPLE_400
    else:
        border_color = ft.Colors.WHITE_10
    
    # Build card content based on status
    card_content = [
        # Story code badge
        ft.Container(
            content=ft.Text(story_code, size=10, weight="bold", color=ft.Colors.CYAN_300),
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.CYAN_400),
            padding=ft.Padding(6, 2, 6, 2),
            border_radius=4,
        ),
        # Title
        ft.Text(title, size=14, weight="bold", color=ft.Colors.WHITE),
        # Description (truncated - full text in README)
        ft.Container(
            content=ft.Text(
                description[:80] + "..." if len(description) > 80 else description,
                size=11, color=ft.Colors.GREY_400
            ),
            tooltip=description,  # Full description as tooltip
        ),
        # XP badge
        ft.Row([
            ft.Container(
                content=ft.Text(f"XP: {xp}", size=10, color=ft.Colors.AMBER_300),
                bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.AMBER_400),
                padding=ft.Padding(6, 2, 6, 2),
                border_radius=4,
            ),
        ]),
    ]
    
    # Add retry hint if struggling
    if retries >= 3 and status != 'shipped':
        card_content.append(
            ft.Text("💡 Need help? Check the hints!", size=10, color=ft.Colors.PURPLE_300, italic=True)
        )
    
    # Add buttons based on status
    if status == 'backlog' or status == 'ready':
        # START MISSION button
        card_content.append(
            ft.Container(height=8),
        )
        card_content.append(
            ft.ElevatedButton(
                "🚀 START",
                on_click=lambda e, s=story: on_start(s),
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                width=120,
                height=32,
            )
        )
    elif status == 'in_progress':
        # TEST + FOLDER buttons
        card_content.append(ft.Container(height=8))
        card_content.append(
            ft.Row([
                ft.ElevatedButton(
                    "TEST",
                    icon=ft.Icons.SCIENCE,
                    on_click=lambda e, s=story: on_test(s),
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE,
                    width=100,
                    height=32,
                ),
                ft.IconButton(
                    ft.Icons.FOLDER_OPEN,
                    icon_color=ft.Colors.GREY_400,
                    on_click=lambda e, s=story: on_continue(s),
                    tooltip="Open in VS Code",
                ),
            ], spacing=4)
        )
    elif status == 'shipped':
        # Completed badge
        card_content.append(ft.Container(height=8))
        card_content.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_400, size=16),
                    ft.Text(f"+{xp} XP", size=12, color=ft.Colors.GREEN_300, weight="bold"),
                ], spacing=6),
                bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.GREEN_400),
                padding=ft.Padding(8, 4, 8, 4),
                border_radius=6,
            )
        )
    
    return ft.Container(
        content=ft.Column(card_content, spacing=6),
        padding=14,
        bgcolor="#0f172a",
        border_radius=8,
        border=ft.Border.all(2 if retries >= 2 or status == 'shipped' else 1, border_color)
    )
